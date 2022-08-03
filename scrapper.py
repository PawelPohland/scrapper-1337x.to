from scrapper_selenium import ScrapperSelenium
from scrapper_requests import ScrapperRequests

from bs4 import BeautifulSoup

import re
import urllib.parse


class Scrapper:

    table_cells = {
        "name": 0,
        "seeds": 1,
        "leeches": 2,
        "date": 3,
        "size": 4,
        "uploader": 5
    }

    sort_types = ["time", "size", "seeders", "leechers"]
    sort_directions = ["asc", "desc"]

    url_types = ["search", "sort-search", "category-search",
                 "sort-category-search", "cat", "sub"]

    search_categories = ["Movies", "TV", "Games", "Music", "Apps",
                         "Documentaries", "Anime", "Other", "XXX"]

    min_keyword_length = 3

    def __init__(self, base_url, selenium_driver_path):
        self.base_url = base_url if not base_url.endswith("/") \
            else base_url.rstrip("/")

        self.search_scrapper = ScrapperSelenium(selenium_driver_path)
        self.category_scrapper = ScrapperRequests()

        self.html_parser = None  # BeautifulSoup
        self.wrapper = None  # data + pagination

    # returns url based on given parameters
    # following urls are valid:
    # https://1337x.to/search/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/cat/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/sub/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/sort-search/{KEYWORD}/{SORT_TYPE}/{ASC|DESC}/{START_PAGE}/
    # https://1337x.to/category-search/{KEYWORD}/{CATEGORY}/{START_PAGE}/
    # https://1337x.to/sort-category-search/{KEYWORD}/{CATEGORY}/{SORT_TYPE}/{ASC|DESC}/{START_PAGE}/
    def get_data_url(self, params):
        try:
            self.url_data = {}
            self.url_data["url"] = [self.base_url]

            if params.get("url_type", "unsupported") in Scrapper.url_types:
                self.url_data["url_type"] = params["url_type"]
                self.url_data["url"].append(params["url_type"])
            else:
                raise Exception("Wrong 'url_type' value. Allowed: " +
                                f"'{','.join(Scrapper.url_types)}'")

            if params.get("keyword", None):
                if params["url_type"] == "cat":
                    if params["keyword"] not in Scrapper.search_categories:
                        raise Exception("Wrong 'keyword' for 'cat' url. " +
                                        f"Allowed: '{','.join(Scrapper.search_categories)}'")

                if (params["url_type"] not in ["cat", "sub"] and
                        len(params["keyword"]) < Scrapper.min_keyword_length):
                    raise Exception("'keyword' parameter has to be at least " +
                                    f"{Scrapper.min_keyword_length} characters long!")

                self.url_data["url"].append(
                    urllib.parse.quote(params["keyword"]))
            else:
                raise Exception("'keyword' parameter is required!")

            if params["url_type"] in ["category-search", "sort-category-search"]:
                if params.get("category", None):
                    if params["category"] in Scrapper.search_categories:
                        self.url_data["url"].append(params["category"])
                    else:
                        raise Exception("Wrong 'category' parameter. Allowed: " +
                                        f"{','.join(Scrapper.search_categories)}")
                else:
                    raise Exception("'category' parameter is required for " +
                                    f"'{params['url_type']}' url!")

            sort_type = params.get("sort_type", None)
            if sort_type:
                if params["url_type"] in ["sort-search", "category-search",
                                          "sort-category-search"]:
                    if sort_type in Scrapper.sort_types:
                        sort_dir = params.get("sort_direction", None)
                        if sort_dir and sort_dir in Scrapper.sort_directions:
                            self.url_data["url"].append(sort_type)
                            self.url_data["url"].append(sort_dir)
                        else:
                            raise Exception("Wrong 'sort_direction' parameter. " +
                                            f"Allowed: '{','.join(Scrapper.sort_directions)}'")
                    else:
                        raise Exception("Wrong 'sort_type' paramter. Allowed: " +
                                        f"'{','.join(Scrapper.sort_types)}'")
                else:
                    raise Exception("'sort_type' parameter is allowed only for " +
                                    "'sort-search,category-search,sort-category-search' urls!")

            elif params["url_type"] in ["sort-search", "category-search",
                                        "sort-category-search"]:
                raise Exception("'sort_type' and 'sort_direction' parameters " +
                                "are required for 'sort-search,category-search," +
                                "sort-category-search' urls!")

            start_page = int(params.get("start_page", 1))
            if start_page < 1:
                start_page = 1

            self.url_data["start_page"] = start_page
        except Exception as error:
            print(f"Scrapper ~ error: {error}")

    # returns url for given page_num
    def get_url(self, page_num):
        url = self.url_data["url"][:]
        url.append(str(page_num))
        url = "/".join(url) + "/"

        return url

    # check if tag is the last pagination link
    def is_last_pagination_link(self, tag):
        # <li class="last"><a href="#">Last</a></li>
        return tag.has_attr("class") and "last" in tag["class"]

    # get last page number from pagination links
    def get_last_page_number(self):
        last_page_num = None

        pagination = self.wrapper.find("div", {"class": "pagination"})

        # pagination element may not exists
        if pagination:
            last_link = pagination.find(self.is_last_pagination_link)
            if last_link:
                link = last_link.find("a").get("href")
                # href may look like this:
                # /{URL_TYPE}/{KEYWORD}/{SORT_PARAMS}/{LAST_PAGE_NUM}/
                numbers = re.findall(r"[\d]+", link)
                if numbers:
                    # last found number is last page number
                    last_page_num = int(numbers[-1])

        return last_page_num

    # parse data from source page
    def parse_data(self, page_type):
        cls = "box-info-detail" if page_type == "search" else "featured-list"
        self.wrapper = self.html_parser.find("div", {"class": cls})

        parsed_data = []

        if self.wrapper:
            table_rows = self.wrapper.find("tbody").find_all("tr")
            for row in table_rows:
                table_data = row.find_all("td")
                data = {}

                # first td of every tr = name and link; there are two links:
                # icon and link - parse only last (second) link
                link = table_data[Scrapper.table_cells["name"]].find_all(
                    "a")[-1]
                data["name"] = link.text
                data["link"] = f"{self.base_url}{link['href']}"

                data["seeds"] = table_data[Scrapper.table_cells["seeds"]].string
                data["leechers"] = table_data[Scrapper.table_cells["leeches"]].string
                data["time"] = table_data[Scrapper.table_cells["date"]].string

                # size table data may contain some other text as well
                # so use separator then split by it and take the first element
                size = table_data[Scrapper.table_cells["size"]].get_text(
                    "{sep}")
                data["size"] = size.split("{sep}")[0]

                parsed_data.append(data)

        return parsed_data

    # parse links from category/subcategory
    # https://1337x.to/cat/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/sub/{KEYWORD}/{START_PAGE}/
    def parse_category(self, url):
        page_source = self.category_scrapper.get_source_page(url)
        if page_source:
            self.html_parser = BeautifulSoup(page_source, "html.parser")
            return self.parse_data(page_type="cat-or-sub")

    # parse links from search results pages
    # https://1337x.to/search/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/sort-search/{KEYWORD}/{SORT_TYPE}/{ASC|DESC}/{START_PAGE}/
    # https://1337x.to/category-search/{KEYWORD}/{CATEGORY}/{START_PAGE}/
    # https://1337x.to/sort-category-search/{KEYWORD}/{CATEGORY}/{SORT_TYPE}/{ASC|DESC}/{START_PAGE}/
    def parse_search_results(self, url):
        page_source = self.search_scrapper.get_source_page(url)
        if page_source:
            self.html_parser = BeautifulSoup(page_source, "html.parser")
            return self.parse_data(page_type="search")

    # scrap data
    def scrap_data(self, params, pages_to_read=1):
        data = []

        try:
            pages_to_read = 1 if not pages_to_read else int(pages_to_read)

            # build url based on given parameters
            self.get_data_url(params)

            url = self.get_url(self.url_data["start_page"])
            print(f"~ Scrapping page: {url}")

            # scrap first page
            if self.url_data["url_type"] in ["cat", "sub"]:
                data += self.parse_category(url)
            else:
                data += self.parse_search_results(url)

            if not data:
                raise Exception(f"No data found for url {url}")

            # how many pages are available to scrap
            pages_available = self.get_last_page_number()

            if pages_available:
                last_page_to_read = self.url_data["start_page"] + pages_to_read
                if last_page_to_read > pages_available:
                    last_page_to_read = pages_available

                # scrap the rest
                for page_num in range(self.url_data["start_page"] + 1, last_page_to_read + 1, 1):
                    url = self.get_url(page_num)
                    print(f"~ Scrapping page: {url}")

                    curr_data = []

                    if self.url_data["url_type"] in ["cat", "sub"]:
                        curr_data = self.parse_category(url)
                    else:
                        curr_data = self.parse_search_results(url)

                    if not curr_data:
                        # just in case there's sth wrong with other pages
                        break
                    else:
                        data += curr_data
        except Exception as error:
            print(f"Scrapper ~ error: ${error}")
        finally:
            return data
