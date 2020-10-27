from bs4 import BeautifulSoup
import csv
import requests
import cookiejar
import mechanize
from http.cookiejar import CookieJar

FIRST_LOGIN_URL = "https://21onlineapp.com/Account/Login"
SECOND_LOGIN_URL = "https://21online.app/Account/Login?returnurl=%2F"

# Custom headers
HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'
}


def get_html(url, params=None):
    """
    Function to get html request.

    :param url: url to parse
    :param params: optional params
    :return: request
    """
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    """
    Get content from table and save it in dict DATA.

    :param html: html of url
    """
    result = []
    soup = BeautifulSoup(html, 'html.parser', auth=("alvaliving@century21.pt", "Oiuyt098"))
    row = soup.find_all('div', {'class': 'row'})
    for elem in row:
        email_col = elem.find_all('div', {'class': 'col-md-3'})
        for el in email_col:
            if len(el.find_all("span")) > 0:
                temp = [el.find_all("span")[2].text]
                result.append(temp)
    return result


def login():
    with requests.Session() as s:
        site = s.get(FIRST_LOGIN_URL)
        bs_content = BeautifulSoup(site.text, 'html.parser')
        token = bs_content.find('input', {'name': '__RequestVerificationToken'})['value']
        login_data = {
            "__RequestVerificationToken": token,
            'UserName': 'alvaliving@century21.pt',
            'Password': 'Oiuyt098'
        }
        s.post(FIRST_LOGIN_URL, login_data)
    login_v2()


def login_v2():
    with requests.Session() as s:
        another_site = s.get(SECOND_LOGIN_URL)
        bs_content_v2 = BeautifulSoup(another_site.content, 'html.parser')
        token_v2 = bs_content_v2.find('input', {'name': '__RequestVerificationToken'})['value']
        login_data_v2 = {
            'Email': 'alvaliving@century21.pt',
            'Password': 'Oiuyt098',
            '__RequestVerificationToken': token_v2
        }
        s.post(FIRST_LOGIN_URL, login_data_v2)
        page = s.get('https://21online.app/#/home')
        b = BeautifulSoup(page.text, 'html.parser')
        print(b)



def parse():
    """
    Main function to parse web site.

    :return: pass
    """
    login()


if __name__ == '__main__':
    parse()
    # write_file(parse())
