# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


# get web page
def get_web_page(url):
    response = requests.get(url)

    response.encoding = 'utf-8'
    if response.status_code != 200:
        print("Invalid url: ", response.url)
        return -1
    else:
        return response.text


def parse_web_html(doc):
    return BeautifulSoup(doc, "html.parser")


def get_web_title(soup):
    return soup.head.title