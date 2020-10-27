import requests
from bs4 import BeautifulSoup
import csv
import time

URL_OF_CATEGORIES = 'https://www.heinemann-shop.com/en/global/'

HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'
}

LIST_OF_PRODUCTS = [
    ["Image_Path", "Brand", "Product", "Amount", "Price"]
]

ERRORS = 0


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_sub_categories_link(html):
    links_of_sub_categories = {}
    soup = BeautifulSoup(html, 'html.parser')
    categories = soup.find_all('div', {'class': 'c-header-navigation__nav-item'})
    for category in categories:
        topic = category.find_all('span')[0].text
        sub_categories = category.find_all('ul', {'class': 'c-header-navigation__col'})
        for sub_sub in sub_categories:
            sub_list = sub_sub.find_all('li')[1:]
            if len(sub_list) == 0:
                sub_list = sub_sub.find_all('li')
            for e in sub_list:
                sub_data = e.find_all('a')
                for el in sub_data:
                    sub_name = el.find_all('span', {"class": ""})[1].text.strip()
                    href = el['href']
                    links_of_sub_categories[sub_name] = href
    return links_of_sub_categories


def get_page_count(html):
    """
    Count how many pages should be parsed.

    :param html: html of url
    :return: int page_count
    """
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', {"class": "c-pagination"})
    if pagination:
        links = pagination.find_all("li", {"class": "c-pagination__page"})
        return int(links[len(links) - 1].find('a').text)


def create_sub_category_link(href):
    # print(f'https://www.heinemann-shop.com{href}')
    return f'https://www.heinemann-shop.com{href}'


def sub_category_parse(sub_category_link):
    # html = get_html('https://www.heinemann-shop.com/en/global/fine-foods-sweets/fine-food/vinegar-oil/c/cat_6011/')
    html = get_html(sub_category_link)
    if html.status_code == 200:
        pages_count = get_page_count(html.text)
        if pages_count:
            for page in range(1, pages_count + 1):
                # print(f'Page: {page} out of {pages_count}')
                html = get_html(sub_category_link, params={'page': page})
                extract_sub_category_content(html.text)
        else:
            extract_sub_category_content(html.text)


def extract_sub_category_content(html):
    # soup = BeautifulSoup(html, 'html.parser')
    # content_table = soup.find('div', {"id": "article-container"})
    # ul = content_table.find('ul', {'class': "c-article-grid"})
    # product_list = ul.find_all('li', {'class': "c-article-grid__item"})
    # for prod in product_list:
    #     try:
    #         image_path = prod.find('img', {"class": "c-article-tile__image lazyload"})['data-lazyload-src']
    #     except TypeError:
    #         image_path = "Image is missing"
    #     brand = prod.find('span', {"class": "c-article-tile__subtitle"}).text
    #     product = prod.find('span', {"class": "c-article-tile__title"}).text
    #     amount = prod.find('div', {"class": "c-article-tile__supplementary"}).text.strip()
    #     print(str(amount.strip()))
    #     # price = prod.find('div', {"class": "c-article-tile__price"}).text
    #     # temp = [
    #     #     image_path,
    #     #     brand,
    #     #     product,
    #     #     amount,
    #     #     price
    #     # ]
    #     # LIST_OF_PRODUCTS.append(temp)
    global ERRORS
    try:
        soup = BeautifulSoup(html, 'html.parser')
        content_table = soup.find('div', {"id": "article-container"})
        ul = content_table.find('ul', {'class': "c-article-grid"})
        product_list = ul.find_all('li', {'class': "c-article-grid__item"})
        for prod in product_list:
            try:
                image_path = prod.find('img', {"class": "c-article-tile__image lazyload"})['data-lazyload-src']
            except TypeError:
                image_path = "Image is missing"
            brand = prod.find('span', {"class": "c-article-tile__subtitle"}).text
            product = prod.find('span', {"class": "c-article-tile__title"}).text
            amount = prod.find('div', {"class": "c-article-tile__supplementary"}).text.strip()
            price = prod.find('div', {"class": "c-article-tile__price"}).text
            temp = [
                image_path,
                brand,
                product,
                str(amount),
                price
            ]
            LIST_OF_PRODUCTS.append(temp)
    except AttributeError:
        ERRORS += 1


def parse():
    html = get_html(URL_OF_CATEGORIES)
    if html.status_code == 200:
        category_href = get_sub_categories_link(html.text)
        for el in category_href:
            sub_link = create_sub_category_link(category_href[el])
            sub_category_parse(sub_link)


def save_data_to_excel(data):
    """
    Save all data to excel file.

    :param data: extracted data.
    :return:
    """
    with open('products.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == '__main__':
    # read()
    start = time.time()
    parse()
    save_data_to_excel(LIST_OF_PRODUCTS)
    print(f'Time total: {(time.time() - start) / 60} minutes')
    # print(f'From Fine Foods & Sweets got {len(LIST_OF_PRODUCTS)} products parsed from first pages!')
    print(f'{len(LIST_OF_PRODUCTS)} products parsed from whole site. Error products {ERRORS}')
