import requests
from bs4 import BeautifulSoup
import json

urls = ['https://perm.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D=1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&office_type%5B4%5D=11&region=4927',]
        # 'https://perm.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D='
        # '1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&region=4927',
        # 'https://perm.cian.ru/snyat-kommercheskiy-uchastok/']

def get_next_page(list_li, num):
    for li in list_li:
        if li.text == f'{num}':
            return li['href']
    return None

# TODO Сделать парсинг всех объявлений, а не только одной страницы
def parse_page(url, num = 2):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        next_url = None
        for div in soup.find_all('div'):
            if 'data-name' in list(div.attrs):
                if div['data-name'] == 'CommercialOfferCard':
                    pass

                if div['data-name'] == 'Pagination':
                    next_url = get_next_page(div.find_all_next('li'), num)


def main_function():
    num = 1
    for url in urls:
        parse_page(url)
        num += 1


if __name__ == "__main__":
    main_function()