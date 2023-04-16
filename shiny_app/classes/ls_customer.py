"""Class to import customer objects from LS API"""
from typing import Any, Generator, Self, Optional
from dataclasses import dataclass, field
from datetime import datetime
from shiny_app.classes.ls_client import BaseLSEntity


@dataclass
class Customer(BaseLSEntity):
    """Customer object from LS"""

    default_params = {"load_relations": '["Contact"]'}

    @dataclass
    class Phone(BaseLSEntity):
        """Phone"""

        number: str
        number_type: str

    @dataclass
    class Email(BaseLSEntity):
        """Email"""

        address: str
        address_type: str

    customer_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    title: str = ""
    company: Optional[str] = None
    create_time: Optional[datetime] = None
    time_stamp: Optional[datetime] = None
    archived: Optional[bool] = None
    contact_id: Optional[int] = None
    credit_account_id: Optional[int] = None
    customer_type_id: Optional[int] = None
    tax_category_id: Optional[int] = None
    phones: list[Phone] = field(default_factory=lambda: [])
    emails: list[Email] = field(default_factory=lambda: [])

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)

        if self.customer_id and self.fetch_from_api:
            customer_json = next(self.get_entities_json(entity_id=self.customer_id))
            customer = self.from_json(customer_json)
            self.__dict__.update(customer.__dict__)

        if isinstance(self.phones, list) and all(isinstance(item, dict) for item in self.phones):
            phones_json = self.phones.copy()
            self.phones.clear()
            for phone in phones_json:
                if isinstance(phone, dict) and all(isinstance(key, str) for key in phone):
                    self.phones.append(self.Phone.discard_extra_args(**phone))

    @classmethod
    def from_json(cls, customer_json: dict[str, Any]) -> Self:
        """Customer object from dict"""
        if not isinstance(customer_json, dict):
            raise ValueError("Customer must be a dict: " + str(customer_json))

        contact_phones_list_json = customer_json.get("Contact", {}).get("Phones", {})
        contact_phones_json = []
        if isinstance(contact_phones_list_json, dict):
            contact_phones_json = contact_phones_list_json.get("ContactPhone", [])
        if not isinstance(contact_phones_json, list):
            contact_phones_json = [contact_phones_json]

        phones_json = [cls.Phone(phone.get("number"), phone.get("useType")) for phone in contact_phones_json]

        contact_emails_list_json = customer_json.get("Contact", {}).get("Emails", {})
        contact_email_json = []
        if isinstance(contact_emails_list_json, dict):
            contact_email_json = contact_emails_list_json.get("ContactEmail", [])
        if not isinstance(contact_email_json, list):
            contact_email_json = [contact_email_json]

        emails_json = [cls.Email(email.get("address"), email.get("useType")) for email in contact_email_json]

        customer_json_transformed = {
            "customer_id": cls.safe_int(customer_json.get("customerID")),
            "first_name": customer_json.get("firstName", "").strip(),
            "last_name": customer_json.get("lastName", "").strip(),
            "company": customer_json.get("company", "").strip(),
            "title": customer_json.get("title", "").strip(),
            "create_time": cls.string_to_datetime(customer_json.get("createTime")),
            "time_stamp": cls.string_to_datetime(customer_json.get("timeStamp")),
            "archived": customer_json.get("archived", "false").lower() == "true",
            "contact_id": cls.safe_int(customer_json.get("contactID")),
            "credit_account_id": cls.safe_int(customer_json.get("creditAccountID")),
            "customer_type_id": cls.safe_int(customer_json.get("customerTypeID")),
            "tax_category_id": cls.safe_int(customer_json.get("taxCategoryID")),
            "phones": phones_json,
            "emails": emails_json,
        }
        return cls(**customer_json_transformed)

    @classmethod
    def get_customers(cls, date_filter: Optional[datetime] = None) -> Generator[Self, None, None]:
        """Generator to return all customers from LS API"""
        for customer in cls.get_entities_json(date_filter=date_filter, params=cls.default_params):
            yield Customer.from_json(customer)

    def update_phones(self) -> None:
        """call API put to update pricing"""
        if self.phones is None or self.customer_id is None:
            raise ValueError("Customer must have phones and customer_id to update")

        numbers = {}
        for phone in self.phones:
            numbers[phone.number_type] = phone.number

        numbers["Mobile"] = (
            numbers.get("Mobile") or numbers.get("Home") or numbers.get("Work") or numbers.get("Fax") or numbers.get("Pager")
        )
        values = {value: key for key, value in numbers.items()}
        numbers = {value: key for key, value in values.items()}

        put_customer = {
            "Contact": {
                "Phones": {
                    "ContactPhone": [
                        {"number": f"{numbers.get('Mobile') or ''}", "useType": "Mobile"},
                        {"number": f"{numbers.get('Fax') or ''}", "useType": "Fax"},
                        {"number": f"{numbers.get('Pager') or ''}", "useType": "Pager"},
                        {"number": f"{numbers.get('Work') or ''}", "useType": "Work"},
                        {"number": f"{numbers.get('Home') or ''}", "useType": "Home"},
                    ]
                }
            }
        }
        self.put_entity_json(self.customer_id, put_customer)
