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

def parse_page(url, i, res, num = 2):
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
        i += 1
        print(a)
    div_pagination = soup.find('div', {'data-name': 'Pagination'})
    next_url = get_next_page(div_pagination.find_all_next('li'), num)
    if next_url:
        parse_page(next_url, i, res, num + 1)


def main_function():
    num = 1
    for url in urls:
        i = 0
        res = {}
        print(url)
        parse_page(url, i, res)
        num += 1


if __name__ == "__main__":
    main_function()