from scrapper import Scrapper

import webbrowser
import os
import time


def get_html_template(path):
    path = os.path.expanduser(path)
    with open(path, "rt") as file:
        return file.read()


def write_to_file(data):
    path = f"{os.getcwd()}{os.sep}"

    time_gen = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

    template = get_html_template(f"{path}template.html")
    template = template.replace("{! info !}", time_gen)
    template = template.split("{! data !}")

    path = f"{path}data"
    if not os.path.exists(path):
        os.makedirs(path)

    filepath = f"{path}{os.sep}{int(time.time_ns()/1000)}.html"

    with open(filepath, "a") as file:
        file.write(template[0] + "\n")

        for index, item in enumerate(data):
            html = f"""
                <tr>
                    <td>{str(index + 1).zfill(3)}</td>
                    <td><a href="{item['link']}" target="_blank">{item['name']}</a></td>
                    <td>{item['time']}</td>
                    <td>{item['size']}</td>
                    <td>{item['seeds']} / {item['leechers']}</td>
                </tr>"""
            file.write(html)

        file.write(template[1])

    return filepath


if __name__ == "__main__":

    selenium_diver_path = '/home/pp/selenium/chromedriver'
    scrapper = Scrapper("https://1337x.to/", selenium_diver_path)

    # params = {
    #     "url_type": "sub",
    #     "keyword": "34",
    #     "start_page": 1
    # }

    params = {
        "url_type": "search",
        "keyword": "javascript",
        "start_page": 1
    }

    data = scrapper.scrap_data(params=params, pages_to_read=1)
    if data:
        print(data)
        #file = write_to_file(data)
        #webbrowser.open(url=f"file://{file}", new=2)
