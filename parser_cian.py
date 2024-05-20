# from dotenv import load_dotenv
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import os
import re

# load_dotenv()
# Урлы, по которым будет производиться поиск адресов с параметрами
urls = ['https://perm.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D=1&'
        'office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&office_type%5B4%5D=11&region=4927',
        'https://perm.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D='
        '1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&region=4927',
        'https://perm.cian.ru/kupit-kommercheskiy-uchastok/',
        'https://perm.cian.ru/snyat-kommercheskiy-uchastok/',]


def get_next_page(list_li, num):
    """Функция возвращает урл, который будет следующем для парсинга

       Сперва проверяется есть ли последующие страницы, которые надо пропарсить. Проверка проходит по числу, которое
       передаётся в функцию"""
    for li in list_li:
        if li.text == f'{num}':
            href = li.a['href']
            if href[0] != '/':
                href = href[20::]
            return 'https://perm.cian.ru' + href
    return None


def change_flor(string):
    """Функция возвращает целочисленное значение для этажа"""
    floor = ""
    for i in string:
        if i == " ":
            break
        floor += i
    return int(floor)


def area(string):
    """Функция возвращает площадь в виде числа с плавающей точкой

       С помощью регулярных выражений находится число в строке, затем с помощью цикла расширение Га или А. Затем
       сравнивая полученное занчение А или Га и домножаем на необходимый множитель"""
    import re

    if string[-1] == ".":
        string = string[:-1]

    strnum = re.sub(r'[^\d.]', '', string.replace(",", "."))

    i = 0
    for p in string:
        if p not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",", "."]:
            break
        i += 1
    if string[i] == " ":
        i += 1
    strarea = string[i::]

    area = float(strnum)
    if strarea in [" Га", " га"]:
        area *= 1000
    elif strarea in [" А", " а", " сот.", " сот"]:
        area *= 100
    return area


def many_areas(result, soup):
    """Функция возвращает словарь площадей в виде числа с плавающей точкой

          С помощью регулярных выражений находится число в строке, затем с помощью цикла расширение Га или А. Затем
          сравнивая полученное занчение А или Га и домножаем на необходимый множитель"""

    divs = soup.find_all('div', {"data-name": "AreasRow", "class": "a10a3f92e9--row--YiBFW"})
    costs = []
    areas = []
    for div in divs:
        a = area(div.contents[1].contents[0].text)
        areas.append(a)
        c = area(div.contents[2].contents[0].text)
        costs.append(c)
    result["costs"] = costs
    result['areas'] = areas


def make_parameters(result, objects):
    """Функция определяет параметры для результирующего словаря

       С помощью цикла и условий определяются искомые параметры для результирующего словаря. Если в цикл попадает объект
       с именем div, то он переопределяется с помощью поиска в объекте div с классом (a10a3f92e9--text--eplgM)"""

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
            result['floor'] = change_flor(object.contents[1].text)
        elif object.contents[0].text == 'Год постройки':
            if 'year' in list(result):
                if result['year'] != object.contents[1].text:
                    result['year'] = object.contents[1].text
            else:
                result['year'] = object.contents[1].text
        elif (object.contents[0].text == 'Общая площадь' or object.contents[0].text == "Площадь"
              or object.contents[0].text == "Площадь участка") :
            if 'area' in list(result):
                if result['area'] != object.contents[1].text:
                    result['area'] = area(object.contents[1].text)
            else:
                result['area'] = area(object.contents[1].text)
        elif object.contents[0].text == "Площади":
            result['areas'] = True


def pars_address(additional_div, result):
    """Эта функция определяет адрес для записи в результирующем словаре"""
    result['address'] = {}
    all_a = additional_div.find_all('a')
    result['address']['region'] = all_a[0].text
    result['address']['city'] = all_a[1].text
    len_a = len(all_a)
    if len_a > 4:
        result['address']['district'] = all_a[2].text
        if len_a < 6:
            result['address']['street'] = all_a[3].text
            result['address']['house'] = all_a[4].text
        else:
            result['address']['sub_district'] = all_a[3].text
            result['address']['street'] = all_a[4].text
            result['address']['house'] = all_a[5].text
    else:
        result['address']['street'] = all_a[2].text
        result['address']['house'] = all_a[3].text


def parse_ad(url):
    """Функция создает и определяет словарь с параметрами для отдельной записи в конечном словаре

       Сперва с помощью requests получаем уро. Затем с помощью BeautifulSoup начинаем парсинг. Далее с помощью метода
       find_all находим все li содержащие параметры и они определяются в словарь. После подобные манипуляции проводятся
       с div и дополнительными параметрами. В конце определятся цена записи"""
    import re


    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url) as response:
    while True:
        sleep(1.5)
        response = requests.get(url)
        if response.status_code == 200:
            result = {}
            soup = BeautifulSoup(response.text, 'html.parser')

            all_li = soup.find_all('li', {'class': 'a10a3f92e9--item--jW0Mi a10a3f92e9--item--hm6MM',
                                      'data-name': 'AdditionalFeatureItem'})
            make_parameters(result, all_li)

            divs = soup.find_all('div', {'class': 'a10a3f92e9--item--Jp5Qv', 'data-name': 'ObjectFactoidsItem'})
            make_parameters(result, divs)

            if "areas" in list(result):
                many_areas(result, soup)

            additional_div = soup.find_all('div', {"data-name": "TechnicalCharacter",
                                                   "class": "a10a3f92e9--container--tu25B"})
            if additional_div:
                result["additional_info"] = []
                for div in additional_div[0]:
                    result["additional_info"].append(div.text)

            address_div = soup.find('div', {'data-name': 'AddressContainer'})
            pars_address(address_div, result)

            cost = soup.find('div', {'data-testid': 'price-amount', "class": 'a10a3f92e9--amount--ON6i1'})

            if cost:
                if "areas" not in list(result):
                    result['cost'] = cost.contents[0].text
                    result['cost'] = float(re.sub(r'[^\d.]', '', result['cost'].replace(",", ".")))
            else:
                result['cost'] = -1

            return result

def parse_page(url, result, num = 2):
    """Функция парсит основную страницу и вызывает функцию, которая парсит адрес

       После того как пропарсятся все адреса вызывается эта же функция, но уже со следующей страницы"""
    while True:
        sleep(1.5)
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
        result[f'{a["href"]}'] = parameters

    div_pagination = soup.find('div', {'data-name': 'Pagination'})
    next_url = get_next_page(div_pagination.find_all_next('li'), num)
    if next_url:
        parse_page(next_url, result, num + 1)

    return result

def main_function():
    """Основная функция, которая запускает парсинг"""
    n = 0
    for url in urls:
        print(n)
        res = parse_page(url, {})
        dir = os.path.abspath(__file__).replace('parser_for_1_kurs_2_sim\parser_cian.py',
                                                f'project_1_kurs_2_sim\cache\cian\json_{n}.json',
                                                1)

        with open(dir, "w") as file:
            json.dump(res, file, indent=4)
        n += 1


# Условие позволяющие запускать код из терминала
if __name__ == "__main__":
    main_function()