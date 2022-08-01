from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class ScrapperSelenium:

    def __init__(self, selenium_driver_path):
        self.driver_path = selenium_driver_path

    def get_source_page(self, url):
        page_source = None

        try:
            chrome_options = Options()
            chrome_options.add_argument("headless")

            service = Service(executable_path=self.driver_path)

            browser = webdriver.Chrome(service=service, options=chrome_options)
            browser.get(url)
            page_source = browser.page_source
            browser.quit()
        except Exception as err:
            print(f"ScrapperSelenium: Something went wrong: {err}")
        finally:
            return page_source
