from os import replace
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
            'title' : item.find('a', class_ = 'model-short-title no-u').get_text(strip = True),
            'link' : HOST + item.find('a', class_ = 'model-short-title no-u').get('href'),
            #Я хз как правильно тут вытянуть инфу, у меня не получается сделать пока что
            # Возможный костыль это оставить парс цены как есть но убирать лишний текст
            # с помощью replace, но вероятно для этого потребуется переводить все это в новый объект
            'price_rub' : item.find('div',class_ = 'model-price-range').get_text(strip = True),
            
            
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