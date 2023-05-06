import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import re
import json




def get_headers():
    return Headers(browser='firefox', os='win').generate()


hh_main = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers()).text
hh_soup = BeautifulSoup(hh_main, 'lxml')

tag_all_vacansy = hh_soup.find('main', class_='vacancy-serp-content')
tag_vacansy = tag_all_vacansy.find_all('a', class_='serp-item__title')

parsed_data = []

for vacansy in tag_vacansy:
    links = vacansy['href']
    links = re.findall(r'https://spb.hh.ru/vacancy/\d+', links)
    for link in links:
        vacansy_main = requests.get(link, headers=get_headers()).text
        disc_vacansy_soup = BeautifulSoup(vacansy_main, 'lxml')


        salary = disc_vacansy_soup.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text

        company_name = disc_vacansy_soup.find('span', 'vacancy-company-name').text

        city_p = disc_vacansy_soup.find('p', attrs={'data-qa': 'vacancy-view-location'})
        city_span = disc_vacansy_soup.find('span', attrs={'data-qa': 'vacancy-view-raw-address'})
        if city_p:
            city = city_p.text
        elif city_span:
            city = city_span.text
        else:
            city = "Город не указан"

        disc_text = re.findall(r'.*Django.*Flask.*|.*Flask.*Django.*',disc_vacansy_soup.find('div', class_='vacancy-section').text)
        for disc_text in disc_text:
            parsed_data.append(
                {
                    'link': link + '\n',
                    'salary': salary + '\n',
                    'company_name': company_name + '\n',
                    'city': city + '\n',
                    'disc': disc_text + '\n' + '\n',
                }
            )
parsed_data_str = json.dumps(parsed_data)

with open("vacancy.txt", "w", encoding='utf-8') as f:
    f.write(parsed_data_str.encode('utf-8').decode('unicode_escape'))