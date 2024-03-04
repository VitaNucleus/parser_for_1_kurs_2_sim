import requests
from bs4 import BeautifulSoup
import json
urls = ['https://perm.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=offices&office_type%5B0%5D='
        '1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&office_type%5B4%5D=11&region=4927',
        'https://perm.cian.ru/kupit-kommercheskiy-uchastok/',
        'https://perm.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=offices&office_type%5B0%5D='
        '1&office_type%5B1%5D=2&office_type%5B2%5D=3&office_type%5B3%5D=5&region=4927',
        'https://perm.cian.ru/snyat-kommercheskiy-uchastok/']

num = 1
for url in urls:
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # with open(f"{num}.txt", "w", encoding='UTF-8') as file:
    #     file.write(soup.find_all('div'))
    num += 1
    for div in soup.find_all('div'):
        if div['data-name']:
            print(div['data-name'])