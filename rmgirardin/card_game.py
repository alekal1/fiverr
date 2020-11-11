import requests
import json
from bs4 import BeautifulSoup
import csv

BASE_URL = 'http://dbs-cardgame.com/us-en/cardlist'
URL = 'http://dbs-cardgame.com/us-en/cardlist/?search=true'  # URL to parse

HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.58'
}

CATEGORIES = []
CARDS = []


def get_html(url, params=None):
    """
    Function to get html request.

    :param url: url to parse
    :param params: optional params
    :return: request
    """
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def create_category_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    list_of_categories = soup.find('ul', {'id': 'snaviList'})
    for category in list_of_categories:
        if category.find('a') != -1:
            category_link = category.find('a')['href'].replace('.', '')
            CATEGORIES.append(category_link)


def parse_subcategory():
    for cat in CATEGORIES:
        link = f'{BASE_URL}/{cat}'
        html = get_html(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        cards_list = soup.find('ul', {'class': 'list-inner'})
        cards = cards_list.find_all('li')
        for card in cards:
            number = card.find('dt', {'class': 'cardNumber'}).text
            name = card.find('dd', {'class': 'cardName'}).text

            bottom_data = card.find('dd', {'class': 'bottomCol'}).find('dl')
            tournament = bottom_data.find('dd').text

            left_data = card.find('dd', {'class': 'leftCol clearfix'}).find_all('dd')
            series = left_data[0].text
            rarity = left_data[1].text

            right_data = card.find('dd', {'class': 'rightCol clearfix'}).find_all('dl')
            if len(right_data) == 10:
                type = right_data[0].find('dd').text
                color = right_data[1].find('dd').text
                power = right_data[2].find('dd').text
                energy_cost = energy_cost_handle(right_data[3])
                combo_energy = right_data[4].find('dd').text
                combo_power = right_data[5].find('dd').text
                character = right_data[6].find('dd').text
                trait = right_data[7].find('dd').text
                era = right_data[8].find('dd').text
                skill = right_data[9].find('dd').text
                temp = {
                    'number': number,
                    'series': series,
                    'rarity': rarity,
                    'available in tournaments': tournament,
                    'name': name,
                    'type': type,
                    'color': color,
                    'power': power,
                    'energy_cost': energy_cost,
                    'combo_energy': combo_energy,
                    'combo_power': combo_power,
                    'character': character,
                    'special trait': trait,
                    'era': era,
                    'skill': skill
                }
                CARDS.append(temp)
            if len(right_data) == 7:
                type = right_data[0].find('dd').text
                color = right_data[1].find('dd').text
                power = right_data[2].find('dd').text
                character = right_data[3].find('dd').text
                trait = right_data[4].find('dd').text
                era = right_data[5].find('dd').text
                skill = right_data[6].find('dd').text
                temp = {
                    'number': number,
                    'series': series,
                    'rarity': rarity,
                    'available in tournaments': tournament,
                    'name': name,
                    'type': type,
                    'color': color,
                    'power': power,
                    'character': character,
                    'special trait': trait,
                    'era': era,
                    'skill': skill
                }
                CARDS.append(temp)
            if len(right_data) == 5:
                type = right_data[0].find('dd').text
                color = right_data[1].find('dd').text
                power = right_data[2].find('dd').text
                energy_cost = energy_cost_handle(right_data[3])
                skill = right_data[4].find('dd').text
                temp = {
                    'number': number,
                    'series': series,
                    'rarity': rarity,
                    'available in tournaments': tournament,
                    'name': name,
                    'type': type,
                    'color': color,
                    'power': power,
                    'energy_cost': energy_cost,
                    'skill': skill
                }
                CARDS.append(temp)
            if len(right_data) == 4:
                type = right_data[0].find('dd').text
                color = right_data[1].find('dd').text
                energy_cost = energy_cost_handle(right_data[2])
                skill = right_data[3].find('dd').text
                temp = {
                    'number': number,
                    'series': series,
                    'rarity': rarity,
                    'available in tournaments': tournament,
                    'name': name,
                    'type': type,
                    'color': color,
                    'energy_cost': energy_cost,
                    'skill': skill
                }
                CARDS.append(temp)


def energy_cost_handle(var):
    energy_cost_number = var.find('dd').text.split()[0].replace('(', '').replace(')', '').replace('-', '')
    if '-' in var.find('dd').text:
        return f'{energy_cost_number}(-)'
    else:
        return f'{energy_cost_number}({len(var.find_all("img"))})'


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        create_category_list(html.text)
        parse_subcategory()
    write_json()


def write_json():
    """
    Write json file of all data collected

    :return: pass
    """
    with open('cards.json', 'w') as json_file:
        json.dump(CARDS, json_file, indent=4)


if __name__ == '__main__':
    parse()
    print(len(CARDS))
