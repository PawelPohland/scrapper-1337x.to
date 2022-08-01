from scrapper import Scrapper
#import json


def print_data(data):
    for index, item in enumerate(data):
        print(f"{str(index + 1).zfill(3)} : {item['name']} [{item['time']}]")


if __name__ == "__main__":

    scrapper = Scrapper("https://1337x.to/")

    params = {
        "url_type": "sub",
        "keyword": "34",
        "start_page": 1
    }

    data = scrapper.scrap_data(params=params, pages_to_read=1)
    if data:
        #data_json = json.dumps(data)
        #print(data_json)
        print_data(data)
