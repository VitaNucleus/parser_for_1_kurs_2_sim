import requests
cok = ''
import time
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
options = uc.ChromeOptions()
# options.add_argument("--headless")
# def write_json(new_data, filename='json_0.json'):
#     with open(filename,'r+') as file:
#         file_data = json.load(file)
#         file_data["data"].append(new_data)
#         file.seek(0)
#         json.dump(file_data, file, indent=4)
#
# driver = uc.Chrome(options=options, use_subprocess=True)
# # options.add_argument("--headless")
# url = "https://perm.domclick.ru/"
#
#
# driver.get("https://domclick.ru/")
# WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="app"]/main/div[2]/section[1]/div[1]/form/div[2]/button""")))
# # time.sleep(1)
#
# # Get the cookies
# cookies = driver.get_cookies()
# for cok in cookies:
#     if cok['name'] == 'qrator_jsid':
#         x = f"{cok['name']}={cok['value']}"
# driver.quit()
# def start(pag):
#     head = {"Host":"bff-search-web.domclick.ru",
#         "Connection":"keep-alive",
#         "Cookie":x,
#         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
#
#     path =(requests.get(f"https://bff-search-web.domclick.ru/api/offers/v1?address=1d1463ae-c80f-4d19-9331-a1b68a85b553&offset={pag}&limit=30&sort=qi&sort_dir=desc&deal_type=sale&category=commercial&offer_type=office&offer_type=warehouse&offer_type=commercial_land&offer_type=free_purpose&aids=42884", headers=head).json()['result']['items'][0:-1])
#     total = ((requests.get(f"https://bff-search-web.domclick.ru/api/offers/v1?address=1d1463ae-c80f-4d19-9331-a1b68a85b553&offset={pag}&limit=30&sort=qi&sort_dir=desc&deal_type=sale&category=commercial&offer_type=office&offer_type=warehouse&offer_type=commercial_land&offer_type=free_purpose&aids=42884", headers=head).json()['result']['pagination']['total']))
#     if pag < total:
#
#         for i in path:
#             print(i['path'])
#             print(i['offerType'])
#             try:
#                 area = i['objectInfo']['area']
#                 floor = (i['objectInfo']['floor'])
#             except:
#                 area = 0
#                 floor = 0
#             print(i['offerRegionName'])
#             print(i['address']['displayName'])
#             print(i['price'])
#             print('===============================')
#             newdata = {i['path']:{'type':i['offerType'],'floor':floor,'address':{"area":area,"region":i['offerRegionName'],"address":i['address']['displayName']},'cost':i['price']}}
#             write_json(newdata)
#     else:
#         exit()
# pag = int(input('Enter which Page You want [ex:1]: '))
# pag *= 30
# start(pag)
# print('Done first Page')
# xooo = input("Continue To Next Page? (y,n) ")
# if xooo == 'y':
#     while True:
#         pag += 30
#         start(pag)
#

if __name__ == "__main__":
    response = requests.get("https://www.avito.ru/perm/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA&f=ASgBAQICAUSwCNJWAUCeww1U5OM5itk5iNk5htk5hNk5")
    print(response.status_code)