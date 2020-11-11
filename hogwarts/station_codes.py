import requests
import json
from bs4 import BeautifulSoup

"""
Script to parse web site

Made for hogwarts by alekal
"""

URL = 'https://irfca.org/apps/station_codes'  # URL to parse

# Custom headers
HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

DATA = {}  # dict to store all parsed data

def get_html(url, params=None):
    """
    Function to get html request.

    :param url: url to parse
    :param params: optional params
    :return: request
    """
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_page_count(html):
    """
    Count how many pages should be parsed.

    :param html: html of url
    :return: int page_count
    """
    soup = BeautifulSoup(html, 'html.parser')
    div_pagination = soup.find_all('div', {'class': 'pagination'})
    links = div_pagination[2].find_all('a')
    if links:
        return int(links[len(links) - 2].get_text())
    else:
        return 1


def get_content(html):
    """
    Get content from table and save it in dict DATA.

    :param html: html of url
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'zebra-striped'})
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    for item in trs:
        station_code = item.find_all("td")[0].text
        station_name = item.find_all("td")[1].text
        DATA[station_code] = station_name


def parse():
    """
    Main function to parse web site.

    :return: pass
    """
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_page_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Page: {page} out of {pages_count}')
            html = get_html(URL, params={'page': page})
            get_content(html.text)
        print("Write json file")
        write_json()


def write_json():
    """
    Write json file of all data collected

    :return: pass
    """
    with open('data.json', 'w') as json_file:
        json.dump(DATA, json_file, indent=0)


if __name__ == '__main__':
    parse()
