import requests
import json
import re
import string
from bs4 import BeautifulSoup
import os

number = int(input())
topic = input()


def save_article(dir_name, file_name, link):
    r_a = requests.get(link)
    a_soup = BeautifulSoup(r_a.content, 'html.parser')
    if a_soup.find("div", {"class": "article-item__body"}):
        with open(f"{os.path.join(dir_name, file_name)}.txt", 'w', encoding="UTF-8") as fd:
            fd.write(a_soup.find("div", {"class": "article-item__body"}).text.strip())
    else:
        with open(f"{os.path.join(dir_name, file_name)}.txt", 'w', encoding="UTF-8") as fd:
            fd.write(a_soup.find("div", {"class": "article__body cleared"}).text.strip())

for i in range(1, number+1):

    request = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=" + str(i)
    r = requests.get(f'{request}')

    if r.status_code != 200:
        print(f'\nThe URL returned {r.status_code}!')
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        dir_name = 'Page_' + str(i)
        os.mkdir(dir_name)
        for article in articles:
            for span in article.findChildren('span', {'class': 'c-meta__type'}):
                if span.text == topic:
                    file_name = f"{article.a.text.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')}"
                    save_article(dir_name, file_name, "https://www.nature.com" + article.a.get('href'))
