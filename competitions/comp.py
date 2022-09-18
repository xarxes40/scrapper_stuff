# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
import csv
import requests

# headers = {
#     'accept': '*/*',
#     'user-agent':
#         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
# }
#
# req = requests.get(url='https://russia-powerlifting.ru/kalendar/kalendar-sorevnovanij-2022#topofthepage', headers=headers)
# soup = BeautifulSoup(req.text, 'lxml')
# all_competes = soup.find('ol').find_all('li')
#
# with open('all_competes.txt', 'w', encoding='utf-8') as file:
#     for i in all_competes:
#         file.write(f'{i.text}\n')

# with open('all_competes.txt', encoding='utf-8') as file:
#     all_comps = [comp.strip() for comp in file.readlines()]

# russians = []
# for comp in all_comps:
#     if 'Россия' in comp:
#         russians.append(comp)
#
# ours = []
# for comp in russians:
#     if 'армлифтингу' in comp or 'строгому подъему на бицепс' in comp:
#         ours.append(comp)
#
# with open('all_competes.txt', 'w', encoding='utf-8') as file:
#     for i in ours:
#         file.write(f'{i}\n')

with open('all_competes.txt', encoding='utf-8') as file:
    all_comps = [comp.strip() for comp in file.readlines()]

    with open('csv.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                "Название",
                "Город",
                "Дата"
            )
        )

    for i in range(0, 74):
        splited = all_comps[i].split(',')

        location = splited[-2].strip()
        date = splited[-1].strip()
        name = ''.join(splited[:-2:]).strip()

        with open('csv.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    name,
                    location,
                    date
                )
            )






