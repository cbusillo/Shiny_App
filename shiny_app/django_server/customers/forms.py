"""Forms to work on customer app"""
from django import forms
from django.db.models import Q
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from .models import Customer, Phone, Email


class CustomerSearchList(forms.Form):
    """Form for searching customers"""

    first_name = forms.CharField(
        label="First Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by Name..."}),
    )

    last_name = forms.CharField(
        label="Last Name",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by Name..."}),
    )


class CustomerSearch(forms.Form):
    """Form for check_in app."""

    last_name_input = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search Last Name",
                "autocomplete": "off",
                "autocorrect": "off",
            }
        ),
    )
    first_name_input = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search First Name", "autocomplete": "off", "autocorrect": "off"}),
    )
    phone_number_input = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search Phone Number", "autocomplete": "off", "autocorrect": "off"}),
    )
    email_address_input = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search Email Address", "autocomplete": "off", "autocorrect": "off"}),
    )
    customer_output = forms.ModelChoiceField(
        label="Customers", required=False, queryset=None, widget=forms.Select(attrs={"size": 15}), empty_label=None
    )

    def __init__(self, *args, **kwargs):
        customers = kwargs.pop("customers", None)
        super().__init__(*args, **kwargs)

        if customers:
            self.fields["customer_output"].queryset = customers

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_id = "customer_search_form"
        self.helper.attrs = {"autocomplete": "off", "data-url": reverse_lazy("check_in:partial_customer_form_data")}

    def get_customer_options(self, last_name, first_name, phone_number, email_address):
        """Get customer options for select"""
        customer_filter = (
            Q(last_name__icontains=last_name)
            & Q(first_name__icontains=first_name)
            & Q(phones__number__icontains=phone_number)
            & Q(emails__address__icontains=email_address)
        )
        if filter_has_value(customer_filter):
            order_by = "last_name", "first_name"
        else:
            order_by = ("-update_time",)
        customers = Customer.objects.filter(customer_filter).distinct().order_by(*order_by)[:100]
        self.fields["customer_output"].queryset = customers
        return str(self["customer_output"].as_widget())

    def get_customer_list(self, first_name, last_name, phone_number, email_address):
        """Get customer list for display"""
        customer_filter = (
            Q(last_name__icontains=last_name)
            & Q(first_name__icontains=first_name)
            & Q(phones__number__icontains=phone_number)
            & Q(emails__address__icontains=email_address)
        )
        order_by = "last_name", "first_name"
        customers = Customer.objects.filter(customer_filter).distinct().order_by(*order_by)
        return customers


def filter_has_value(query_filter: Q) -> bool:
    """Check for any values in filter"""
    for child in query_filter.children:
        if isinstance(child, Q):
            if filter_has_value(child):
                return True
        else:
            _, value = child
            if value:
                return True
    return False


class CustomerForm(forms.ModelForm):
    """Form to display and edit customer data"""

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "title", "company", "archived", "update_from_ls_time"]
        readonly_fields = "update_from_ls_time"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["first_name"].widget.attrs["class"] = "no-border text-end form-control-lg"
        self.fields["first_name"].field_id = "search_first_name_detail"
        self.fields["last_name"].widget.attrs["class"] = "no-border form-control-lg"
        self.fields["last_name"].field_id = "search_last_name_detail"


class PhoneForm(forms.ModelForm):
    """Form to display and edit phone data"""

    number = PhoneNumberField()

    class Meta:
        model = Phone
        fields = ["number", "use_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["use_type"].widget.attrs["class"] = "no-border text-center form-control-sm"


class EmailForm(forms.ModelForm):
    """Form to display and edit email data"""

    class Meta:
        model = Email
        fields = ["address", "use_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields["use_type"].widget.attrs["class"] = "no-border text-center form-control-sm"