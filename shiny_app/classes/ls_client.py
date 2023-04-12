"""Client for Lightspeed API Inherited from requests.Session"""
from datetime import datetime
import logging
import time
from urllib.parse import urljoin
import requests
from shiny_app.django_server.ls_functions.views import send_message

from shiny_app.modules.load_config import Config


def string_to_datetime(date_string: str) -> datetime:
    """Convert date string to datetime object"""
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def datetime_to_string(date_string: datetime) -> str:
    """Convert datetime object to string"""
    return date_string.strftime("%Y-%m-%dT%H:%M:%S%z")


class Client(requests.Session):
    """Client class for Lightspeed API Inherited from requests.Session"""

    def __init__(self) -> None:
        super().__init__()

        def rate_hook(response_hook, *_args, **_kwargs):
            if "x-ls-api-bucket-level" in response_hook.headers:
                rate_level, rate_limit = response_hook.headers["x-ls-api-bucket-level"].split("/")
                rate_level = int(float(rate_level))
                rate_limit = int(float(rate_limit))

                logging.info("rate: %i/%i", rate_level, rate_limit)
                if rate_limit - rate_level < 10:
                    logging.warning("Rate limit reached, sleeping for 1 second")
                    send_message("Rate limit reached, sleeping for 1 second")
                    time.sleep(1)

            if response_hook.status_code == 200:
                return

            if response_hook.status_code == 429:
                retry_seconds = int(float(response_hook.headers["Retry-After"]))
                logging.info("rate limit reached, sleeping for %i", retry_seconds)
                send_message(f"Rate limit reached, sleeping for {retry_seconds}")
                time.sleep(retry_seconds)
            if response_hook.status_code == 401:
                self.auth_header = self.get_auth_header()
                self.headers.update(self.auth_header)
            logging.error("received bad status code: %s", response_hook.text)

        self.token = Config.ACCESS_TOKEN
        self.auth_url = Config.LS_URLS["access"]
        self.base_url = f"https://api.lightspeedapp.com/API/V3/Account/{Config.LS_ACCOUNT_ID}/"
        self.auth_header = self.get_auth_header()
        self.headers.update(self.auth_header)
        self._response: requests.Response
        self.hooks["response"].append(rate_hook)

    def get_auth_header(self) -> dict[str, str]:
        """get or reauthorize the auth header"""
        auth_response = requests.post(self.auth_url, data=self.token, timeout=60)
        return {"Authorization": f"Bearer {auth_response.json()['access_token']}"}

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response | None:
        """extened request method to add base url and timeouts"""
        if "://" not in url:
            url = urljoin(self.base_url, url)
        if "timeout" not in kwargs:
            kwargs["timeout"] = 10
        response_code = 0
        retries = 5
        while response_code != 200:
            request_response = super().request(method, url, *args, **kwargs)
            response_code = request_response.status_code
            retries -= 1
            if retries == 0:
                raise TimeoutError
            if response_code == 404:
                return None
        return request_response  # pyright: reportUnboundVariable=false

    def _entries(self, url: str, key_name: str, params: dict | None = None):
        """Iterate over all items in the API"""

        next_url = url
        page = 0
        while next_url != "":
            send_message(f"Getting page {page} of {key_name}")
            self._response = self.get(next_url, params=params)
            if not isinstance(self._response, requests.models.Response):
                return
            entries = self._response.json().get(key_name)
            if not entries:
                return
            if not isinstance(entries, list):
                yield entries
                return

            for entry in entries:
                yield entry

            next_url = self._response.json()["@attributes"]["next"]
            page += 1

    def get_items_json(self, category_id: str = "", description: str = "", date_filter: datetime | None = None):
        """Get all items"""
        params = {"load_relations": '["ItemAttributes"]', "limit": "100"}
        if date_filter:
            params["timeStamp"] = f">,{date_filter}"

        if category_id:
            params["categoryID"] = category_id
        if description:
            params["or"] = description

        return self._entries(Config.LS_URLS["items"], "Item", params=params)

    def get_customers_json(self, date_filter: datetime | None = None):
        """Get all items"""
        params = {"load_relations": '["Contact"]', "limit": "100"}
        if date_filter:
            params["timeStamp"] = f">,{date_filter}"
        return self._entries(Config.LS_URLS["customers"], "Customer", params=params)

    def get_customer_json(self, customer_id: int):
        """Get customer"""
        url = Config.LS_URLS["customer"].format(customerID=customer_id)
        params = {"load_relations": '["Contact"]'}
        return next(self._entries(url, key_name="Customer", params=params))

    def get_workorder_json(self, workorder_id: int):
        """Get workorder"""
        url = Config.LS_URLS["workorder"].format(workorderID=workorder_id)
        return next(self._entries(url, key_name="Workorder"))

    def get_workorders_json(self, date_filter: datetime | None = None):
        """Get all workorders"""
        params = {"limit": "100"}
        if date_filter:
            params["timeStamp"] = f">,{date_filter}"
        return self._entries(Config.LS_URLS["workorders"], "Workorder", params=params)

    def get_item_json(self, item_id: int):
        """Get item"""
        url = Config.LS_URLS["item"].format(itemID=item_id)
        params = {"load_relations": '["ItemAttributes"]'}
        return self._entries(url, key_name="Item", params=params)

    def get_size_attributes_json(self):
        """Get all size attributes"""
        url = Config.LS_URLS["itemMatrix"]
        return self._entries(url, "ItemMatrix", params={"load_relations": '["ItemAttributeSet"]'})
