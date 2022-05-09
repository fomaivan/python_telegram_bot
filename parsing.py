import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import config


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Название', 'Ссылка на страницу'])
        for item in items:
            writer.writerow([item['title'], item['link']])


def get_pages_count(html_):
    soup = BeautifulSoup(html_, 'html.parser')
    pagination = soup.find_all('li', class_='page')
    if pagination:
        return pagination[-1].text


def get_content(html_):
    soup = BeautifulSoup(html_, 'html.parser')
    items = soup.find_all("div", class_="sc-16r8icm-0 escjiH")
    crypto_list = []
    for item in items:
        try:
            crypto_list.append({
                'link': config.HOST + item.find('a', class_='cmc-link').get('href'),
                'title': item.find('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol').text
            })
        except:
            pass
    items = soup.find_all("tr", class_="sc-1rqmhtg-0 jUUSMS")
    for item in items:
        try:
            crypto_list.append({
                'link': config.HOST + item.find('a', class_='cmc-link').get('href'),
                'title': item.find('span', class_='crypto-symbol').text
            })
        except:
            pass

    return crypto_list


def parse():
    html_ = requests.get(config.URL)
    if html_.status_code == 200:
        pages_count = get_pages_count(html_.text)
        crypto_list = []
        for i in range(1, int(pages_count) + 1):
            print("Парсинг страницы {}".format(i))
            html_ = requests.get(config.URL, params={'page': i})
            crypto_list.extend(get_content(html_.text))
        save_file(crypto_list, config.FILE)


parse()
a = pd.read_csv('crypto_list.csv', delimiter=',')
