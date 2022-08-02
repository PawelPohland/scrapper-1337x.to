# Scrapper - https://1337x.to/

## Features

- gets links from various https://1337x.to/ pages (search results pages, category and subcategory pages)
- pulls out data about torrent links: name, link, size, uploaded time, number of seeds and leechers
- can mark selected keywords in scrapped data
- saves data to HTML file
- saves data to JSON file
- opens saved HTML file in default web browser

## Technologies used

- Python (requests, Selenium webdriver, BeautifulSoup, webbrowser)
- HTML
- CSS

## Possible improvements

- add method to list only links that fits into given keywords (for example - find only links with "go" phrase)
- add command line interface (argparse)
- add graphical user interface (for instance with PyQt)
- add Cron job to scrap data periodically
- send generated reports (html files) to e-mail address
- marking keywords with different colors (tags)
- marking keywords - add word boundings to pattern
- remove duplicated links from scrapped data
