import requests
from requests.exceptions import HTTPError

class ScrapperRequests:

    def __init__(self):
        self.session = requests.Session()

    def get_source_page(self, url):
        page_source = None

        try:
            response = self.session.get(url)
            response.raise_for_status()

            page_source = response.text

        except HTTPError as http_err:
            print(f"HTTP error occured: {http_err}")
            print(f"Response status code: {response.status_code}")
        except Exception as err:
            print(f"An error has occured: {err}")
        finally:
            return page_source
