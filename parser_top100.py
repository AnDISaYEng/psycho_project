import requests
import json
from bs4 import BeautifulSoup

main_url = 'http://senpai.cc/top-anime2021.html'


def open_page(url):
    response = requests.get(url)
    return response.text


def get_soup(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup


def get_cards(soup):
    listing = soup.find('div', class_='main-items').find('div', id='content').find('div', id='dle-content')
    cards = listing.find_all('div', class_='kino-item')
    return cards


def get_data(cards):
    title = cards.find('div', class_='kino-title').find('a').text
    place = cards.find('div', class_='kino-inner').find('div', class_='kino-img').find('div',
                                                                                       class_='k-meta qual-mark').text
    return {'title': title}


def main():
    cards1 = []
    page = open_page(main_url)
    soup = get_soup(page)
    cards2 = get_cards(soup)
    cards1.extend(cards2)
    data = []
    for card in cards1:
        data.append(get_data(card))
    top = json.dumps(data, ensure_ascii=False)
    s = []
    for i in data:
        for v in i.values():
            v.replace('n', '')
            s.append(v[1:-1])
    return s


main()
