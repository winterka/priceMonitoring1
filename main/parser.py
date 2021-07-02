from os import replace
import unicodedata
from bs4 import BeautifulSoup
import requests
from main.models import Complete

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
            'price_rub' : item.find('div', class_ = 'model-price-range').get_text(strip = True).replace(u'\xa0',u''),
        }) 
    for i in range(len(cards)):
        temp = str(cards[i])
        #print(temp)
        temp.replace('title' , '')
        currentTitle = str(temp[11 : temp.find(",") - 1 ])
        if (temp.find("д") != -1 ):
            lowestPrice = int(temp[temp.find('т') + 1 : temp.find("д")])
        else:
            lowestPrice = int(temp[temp.find('т') + 1 : temp.find("р")])
        if (temp.find('до') != -1):
            highestPrice = int(temp[temp.find('до') + 2 : temp.find("р")])
        else:
            highestPrice = lowestPrice
        averagePrice = int((lowestPrice + highestPrice) / 2)
        name = currentTitle
        price = averagePrice
        print(currentTitle)
        print(averagePrice)
    
    return cards  

    

def parse():
    pg = int(input('Сколько страниц парсить '))
    for i in range(pg):
        page = str(i)
        html = get_html(URL + page + '/')
        #Проверка заходит ли парсер на сайт
        if html.status_code == 200:
            get_content(html.text)
        else:
            print('Error')
parse()