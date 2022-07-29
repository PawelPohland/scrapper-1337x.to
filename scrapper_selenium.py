from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ScrapperSelenium:

    def __init__(self):
        ...

    def get_source_page(self, url):
        page_source = None

        try:
            chrome_options = Options()
            chrome_options.add_argument("headless")

            browser = webdriver.Chrome(options=chrome_options)
            browser.get(url)
            page_source = browser.page_source
            browser.quit()
        except Exception as err:
            print(f"ScrapperSelenium: Something went wrong: {err}")
        finally:
            return page_source
