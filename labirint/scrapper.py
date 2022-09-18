# -*- coding: utf-8 -*-
import time

from bs4 import BeautifulSoup
import requests
import json
import csv


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

with open('Programming_books.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            "Название",
            "Автор",
            "Цена",
            "Скидка"
        )
    )

page_count = 0
for page in range(1, 16):
    result = []

    url = f'https://www.labirint.ru/genres/2308/?page={page}&display=table'
    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')

    all_books = soup.find(class_='products-table__body').find_all('tr')
    books_counter = 0
    try:
        for i in all_books:
            books_counter += 1
            book_name = i.find(class_='book-qtip').text
            book_price = str(i.find(class_='price-val').text).replace(u'\u20bd', 'rub').strip()
            new_price = int(i.find(class_='price-val').next_element.next_element.text.replace(' ', ''))
            old_price = int(i.find(class_='price-old').next_element.next_element.text.replace(' ', ''))
            book_sale = round(100 - (new_price / (old_price / 100)), 2)
            book_author = i.find(class_='col-sm-2').find(class_='mt3').text.strip()

            res_dict = {
                "Название": book_name,
                "Автор": book_author,
                "Цена": book_price,
                "Скидка": book_sale
            }

            result.append(res_dict)

            with open('Programming_books.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        book_name,
                        book_author,
                        book_price,
                        book_sale
                    )
                )

    except Exception as ex:
        print(f'[ERROR] Something went wrong here... Check book {books_counter} on page {page_count + 1}')
        continue

    with open('resul.json', 'a', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    page_count += 1

    print(f'[INFO] Page number {page_count} has been scrapped')
    time.sleep(4)

