import requests
from bs4 import BeautifulSoup
import json

urls = ['https://perm.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D=1&'
        'office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&office_type%5B4%5D=11&region=4927',]
        # 'https://perm.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D='
        # '1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&region=4927',
        # 'https://perm.cian.ru/snyat-kommercheskiy-uchastok/',
        # 'https://perm.cian.ru/kupit-kommercheskiy-uchastok/']


def get_next_page(list_li, num):
    for li in list_li:
        if li.text == f'{num}':
            href = li.a['href']
            if href[0] != '/':
                href = href[20::]
            return 'https://perm.cian.ru' + href
    return None


def area(string):
    import re

    snum = re.sub(r'[^\d.]', '', string.replace(",", "."))

    i = 0
    for p in string:
        if p not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",", "."]:
            break
        i += 1
    if string[i] == " ":
        i += 1
    sarea = string[i::]

    area = float(snum)

    if sarea in ["Га", "га"]:
        area *= 1000
    if sarea in ["А", "а"]:
        area *= 100
    a = 0
    return area


def make_parameters(result, objects):

    for object in objects:
        if object.name == "div":
            object = object.find("div", {"class": "a10a3f92e9--text--eplgM"})
        if object.contents[0].text == 'Тип здания':
            result['type'] = object.contents[1].text
        elif object.contents[0].text == 'Категория здания':
            result['category'] = object.contents[1].text
        elif object.contents[0].text == 'Этажность':
            result['floors'] = object.contents[1].text
        elif object.contents[0].text == 'Этаж':
            result['floor'] = object.contents[1].text
        if object.contents[0].text == 'Год постройки':
            if 'year' in list(result):
                if result['year'] != object.contents[1].text:
                    result['year'] = object.contents[1].text
            else:
                result['year'] = object.contents[1].text
        elif object.contents[0].text == 'Общая площадь' or object.contents[0].text == "Площадь":
            if 'area' in list(result):
                if result['area'] != object.contents[1].text:
                    result['area'] = area(object.contents[1].text)
            else:
                result['area'] = area(object.contents[1].text)


def parse_ad(url):
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            break

    result = {}

    soup = BeautifulSoup(response.text, 'html.parser')

    all_li = soup.find_all('li', {'class': 'a10a3f92e9--item--jW0Mi a10a3f92e9--item--hm6MM',
                              'data-name': 'AdditionalFeatureItem'})
    make_parameters(result, all_li)
    print(url, result)
    divs = soup.find_all('div', {'class': 'a10a3f92e9--item--Jp5Qv', 'data-name': 'ObjectFactoidsItem'})

    make_parameters(result, divs)
    print(url, result)
    # print(divs)

    return result

def parse_page(url, i, result, num = 2):
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            break

    soup = BeautifulSoup(response.text, 'html.parser')
    next_url = None
    main_div = soup.find('div', {'class': '_32bbee5fda--wrapper--W0WqH'})

    for div in main_div.find_all('div', {'data-name': 'CommercialOfferCard',
                                     'class': '_32bbee5fda--offer-container--Zhu18',
                                     }):
        a = div.find('a', {'data-name': 'CommercialTitle'})

        parameters = parse_ad(a['href'])
        # result[f'{a["href"]}'] = parameters
        i += 1
    print(i)
    with open("json.txt", 'w') as file:
        json.dump(result, file, indent=4)
    div_pagination = soup.find('div', {'data-name': 'Pagination'})
    # next_url = get_next_page(div_pagination.find_all_next('li'), num)
    # if next_url:
    #     parse_page(next_url, i, res, num + 1)


def main_function():
    num = 1
    for url in urls:
        i = 0
        res = {}
        # print(url)
        parse_page(url, i, res)
        # parse_ad("https://perm.cian.ru/sale/commercial/300337408/")
        num += 1


if __name__ == "__main__":
    main_function()