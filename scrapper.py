from scrapper_selenium import ScrapperSelenium
from scrapper_requests import ScrapperRequests

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

    def __init__(self, base_url):
        self.base_url = base_url if not base_url.endswith("/") \
            else base_url.rstrip("/")

        self.search_scrapper = ScrapperSelenium()
        self.category_scrapper = ScrapperRequests()

        self.html_parser = None  #  BeautifulSoup
        self.wrapper = None #  data + pagination

        self.last_url_parsed = None
        self.last_page_num = None

    # returns url based on given parameters
    # following urls are valid:
    # https://1337x.to/search/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/cat/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/sub/{KEYWORD}/{START_PAGE}/
    # https://1337x.to/sort-search/{KEYWORD}/{SORT_TYPE}/{ASC|DESC}/{START_PAGE}/
    # https://1337x.to/category-search/{KEYWORD}/{CATEGORY}/{START_PAGE}/
    # https://1337x.to/sort-category-search/{KEYWORD}/{CATEGORY}/{SORT_TYPE}/{ASC|DESC}/{START_PAGE}/
    def get_data_url(self, params):
        url = []

        try:
            url.append(self.base_url)

            if params.get("url_type", "unsupported") in Scrapper.url_types:
                url.append(params["url_type"])
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

                url.append(urllib.parse.quote(params["keyword"]))
            else:
                raise Exception("'keyword' parameter is required!")

            if params["url_type"] in ["category-search", "sort-category-search"]:
                if params.get("category", None):
                    if params["category"] in Scrapper.search_categories:
                        url.append(params["category"])
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
                            url.append(sort_type)
                            url.append(sort_dir)
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

            url.append(str(params.get("start_page", 0)))
            url = '/'.join(url) + "/"
        except Exception as error:
            print(f"Scrapper ~ error: {error}")
        finally:
            return url
