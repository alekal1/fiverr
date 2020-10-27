import requests
from bs4 import BeautifulSoup
import csv

"""

Script to parse web site and extract airport information

Made for youscale by alekal on fiverr.com

"""

# Url where you can get all the countries
URL_TO_GET_COUNTRY = 'https://airports-list.com/largest-countries-by-airports'

# Headers for parsing
HEADERS_TO_GET_COUNTRY_LIST = {
    'Accept': '*/*',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38"
}

# Dictionary to save all the countries link, so we can make a request to the country page
COUNTRY_LINKS = {}

# Data set. All data will be saved in this list for excel writing
AIRPORT_DATA = [
    [
        'Country',
        # 'Airport ID',
        'City',
        'Airport Name',
        'IATA Code',
        'ICAO Code'
    ]
]


def get_country_list(url, params=None):
    """
    Method for country name extraction.

    :param url: Url where we can extract all the countries
    :param params: specific params
    :return: request
    """
    return requests.get(url, headers=HEADERS_TO_GET_COUNTRY_LIST, params=params)


def get_countries_parse():
    """
    Pass the request to extract_countries_and_links method for link extraction.

    :return:
    """
    countries_request = get_country_list(URL_TO_GET_COUNTRY)
    if countries_request.status_code == 200:
        extract_countries_and_links(countries_request.text)


def extract_countries_and_links(html):
    """
    Extract link for every country and save them in dictionary.

    :param html: country request html
    """
    soup = BeautifulSoup(html, 'html.parser')
    country_table = soup.find('table', {'class': "views-view-grid cols-1"})
    tbody = country_table.find('tbody')
    tds = tbody.find_all('td')
    for country in tds:
        country_info = country.find_all('a')
        country_name = country_info[0].text
        country_href = country_info[0]['href']
        COUNTRY_LINKS[country_name] = country_href


def create_country_link(href):
    """
    Create a new URL to specific country.

    :param href: params to specific link
    :return:
    """
    return f'https://airports-list.com{href}'


def get_country_html(url, params=None):
    """
    Method for specific country request.

    :param url: Link of country generated in create_country_link
    :param params: params of the link
    :return: request
    """
    return requests.get(url, params=params)


def parse_country_site(link, country):
    """
    Metho for country parsing.

    :param link: link of country generated in create_country_link
    :param country: country name
    :return:
    """
    html = get_country_html(link)
    if html.status_code == 200:
        get_page_content(html.text, country)


def get_page_content(html, country):
    """
    Extract country page content:
    Id, City, Airport name, Iata code, Icao code.
    Save all data into list.

    :param html: html of country
    :param country: country name
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('tbody')
    trs = table.find_all('tr')
    for elem in trs:
        # id = elem.find('td', {'class': 'views-field views-field-counter'}).text.strip().replace(".", "")
        city = elem.find('td', {'class': 'views-field views-field-field-gorod-eng'}).text.strip()
        airport_name = elem.find('a').text.strip()
        iata_code = elem.find('td', {'class': 'views-field views-field-title-3'}).text.strip()
        icao_code = elem.find('td', {'class': 'views-field views-field-field-icao'}).text.strip()
        temp = [
            country,
            # id,
            city,
            airport_name,
            iata_code,
            icao_code
        ]
        AIRPORT_DATA.append(temp)


def save_data_to_excel(data):
    """
    Saves data into csv file.

    :param data: all parsed countries with their airports
    :return:
    """
    with open('flights.csv', 'w', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    """
    Main method for running script
    """
    get_countries_parse()
    for el in COUNTRY_LINKS:
        link = create_country_link(COUNTRY_LINKS[el])
        parse_country_site(link, el)
    save_data_to_excel(AIRPORT_DATA)


if __name__ == '__main__':
    """
    Runs the script's main method
    """

    main()
