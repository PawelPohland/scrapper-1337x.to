from scrapper import Scrapper

import webbrowser
import os
import time
import json
import re


# returns content of html template file
def get_html_template(path):
    path = os.path.expanduser(path)
    with open(path, "rt") as file:
        return file.read()


# saves scrapped data as a HTML file
def write_as_html(data):
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


# saves scrapped data as a JSON file
def write_as_json(data):
    path = f"{os.getcwd()}{os.sep}data"

    if not os.path.exists(path):
        os.makedirs(path)

    filepath = f"{path}{os.sep}{int(time.time_ns()/1000)}.json"

    with open(filepath, "a") as file:
        file.write(json.dumps(data))

    return filepath


# marks given keywords with HTML mark tag
def mark_keywords(keywords, data):
    pattern = f"{'|'.join(keywords)}"
    regex = re.compile(rf"({pattern})", flags=re.IGNORECASE)

    def mark_keyword(match_obj):
        if match_obj.group():
            return f"<mark>{match_obj.group()}</mark>"

    for item in data:
        item["name"] = regex.sub(mark_keyword, item["name"])


if __name__ == "__main__":

    selenium_diver_path = '/home/pp/selenium/chromedriver'
    scrapper = Scrapper("https://1337x.to/", selenium_diver_path)

    params = {
        # example: "Other" category with video tutorials
        "url_type": "sub",
        "keyword": "34",
        "start_page": 1

        # search for keyword: javascript
        # "url_type": "sort-search",
        # "keyword": "javascript",
        # "sort_type": "time",
        # "sort_direction": "desc",
        # "start_page": 1
    }

    data = scrapper.scrap_data(params=params, pages_to_read=9)
    if data:
        # save as a JSON file
        #file = write_as_json(data)

        # mark keywords in all links
        mark_keywords(keywords=["programming", "python", "django", "flask",
                                "javascript", "java script", "frontend", "backend", "fullstack",
                                "full-stack", "node.js", "react", "vue.js", "vue", "next.js",
                                "nextjs", "angular", "typescript", "mern", "mevn", "mean", "web", "css",
                                "php", "laravel", "sql", "mysql", "postgresql", "mongodb", "go",
                                "golang", "java", "data structures", "algorithms", "machine learning",
                                "data science", "api", "git", "github", "docker", "kubernetes",
                                "aws", "azure", "jira", "linux", "ubuntu"], data=data)

        # write as a HTML file
        file = write_as_html(data)

        # open HTML file in a default browser
        webbrowser.open(url=f"file://{file}", new=2)
