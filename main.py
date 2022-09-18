import requests
from bs4 import BeautifulSoup
import json

headers = {
    'accept': '*/*',
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

# all_hrefs = []
#
# for i in range(0, 192, 24):
#     url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=July'
#
#     req = requests.get(url=url, headers=headers)
#     json_data = json.loads(req.text)
#     html_response = json_data['html']
#
#     with open(f'index_{i}.html', 'w', encoding='utf-8') as file:
#         file.write(html_response)
#
# for i in range(0, 192, 24):
#     with open(f'index_{i}.html', encoding='utf-8') as file:
#         src = file.read()
#
#         soup = BeautifulSoup(src, 'lxml')
#         hrefs = soup.find_all(class_="card-details-link")
#
#         for href in hrefs:
#             festival_href = href.get('href')
#             all_hrefs.append(festival_href)
#
# with open('all_hrefs.txt', 'w') as file:
#     for line in all_hrefs:
#         file.write(f'https://www.skiddle.com{line}\n')

result = []
with open('all_hrefs.txt', encoding='utf-8') as file:
    lines = [line.strip() for line in file.readlines()]
    count = 0

    for line in lines:
        count += 1
        print(f'Iteration {count} is on. URL: {line}')
        try:
            req = requests.get(url=line, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')

            fest_name = soup.find('h1').text.strip()
            fest_date = soup.find('h3').text.strip()
            fest_location = soup.find(class_="top-info-cont span span9 no-clear").find('a', class_='tc-white').text.strip()
            fest_href = soup.find(class_="top-info-cont span span9 no-clear").find('a', class_='tc-white').get('href')
            url = 'https://www.skiddle.com/' + fest_href

            req = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(req.text, 'lxml')

            contact_details = soup.find('h2', string='Venue contact details and info').find_next()
            items = [item.text for item in contact_details.find_all('p')]

            contact_details_dict = {}

            for item in items:
                item_list = item.split(':')

                if len(item_list) == 3:
                    contact_details_dict[item_list[0].strip()] = item_list[1].strip() + ':' \
                                                            + item_list[2].strip()

                else:
                    contact_details_dict[item_list[0]] = item_list[1]

            result.append(
                {
                    'Festival name': fest_name,
                    'Festival date': fest_date,
                    'Festival location': fest_location,
                    'Contact details': contact_details_dict
                }
            )

        except Exception as ex:
            print(ex)
            print('Something happened. Check URL.')

with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
