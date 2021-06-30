from os import replace
import unicodedata
from bs4 import BeautifulSoup
import requests

#Константы

URL = 'https://www.e-katalog.ru/list/189/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
HOST = 'https://www.e-katalog.ru'

#Функция будет принимать url для парсинга + параметры(Страницы)
def get_html(url, params=None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

#Получает контент со страницы, записывает названия, ссылки(не уверен что они нужны но пока что
# написал, нужно дописать нахождение цены)
def get_content(html):
    soup = BeautifulSoup(html,'html.parser')
    #Идем по карточкам товаров и вытягиваем инфу
    items = soup.find_all('table', class_='model-short-block')
    cards = []
    for item in items:
        cards.append({
            'title' : item.find('a', class_ = 'model-short-title no-u').get_text(strip = True) ,
            'link' : HOST + item.find('a', class_ = 'model-short-title no-u').get('href'),
            'price_rub' : soup.select_one(selector="#price_1941016").get_text(strip=True).replace(u"\xa0",u""),
            
            
            
        })
        
    print(cards)
    print(len(cards))

def parse():
    html = get_html(URL)
    #Проверка заходит ли парсер на сайт
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')
parse()