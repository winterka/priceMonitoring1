import datetime
import urllib.parse
from collections import namedtuple

import bs4
import requests
from django.core.management.base import BaseCommand

from main.models import Complete


InnerBlock = namedtuple('Block', 'title,price,currency,date,url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'


class KatalogParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept-Language': 'ru',
        }

    def get_page(self, page: int = None):
        params = {
            'radius': 0,
            'user': 1,
        }
        if page and page > 1:
            params['p'] = page

        # url = 'https://www.avito.ru/moskva/avtomobili/bmw/5'
        url = 'https://www.e-katalog.ru/list/189/'
        # url = 'https://www.avito.ru/moskva/odezhda_obuv_aksessuary/zhenskaya_odezhda'
        r = self.session.get(url, params=params)
        return r.text

    @staticmethod
    def parse_block(self, item):
        # Выбрать блок со ссылкой
        url_block = item.select_one('a.item-description-title-link')
        href = url_block.get('href')
        if href:
            url = 'https://www.e-katalog.ru' + href
        else:
            url = None

        # Выбрать блок с названием
        title_block = item.select_one('h3.title.item-description-title span')
        title = title_block.string.strip()

        # Выбрать блок с названием и валютой
        price_block = item.select_one('span.price')
        price_block = price_block.get_text('\n')
        price_block = list(filter(None, map(lambda i: i.strip(), price_block.split('\n'))))
        if len(price_block) == 2:
            price, currency = price_block
            price = int(price.replace(' ', ''))
        elif len(price_block) == 1:
            # Бесплатно
            price = 0
        else:
            price = None
            print(f'Что-то пошло не так при поиске цены: {price_block}, {url}')

        # Выбрать блок с датой размещения объявления

        bbb = Block(
            url=url,
            title=title,
            price=price,
        )
        print(bbb)

        try:
            p = Product.objects.get(url=url)
            p.title = title
            p.price = price
            p.currency = currency
            p.save()
        except Product.DoesNotExist:
            p = Product(
                url=url,
                title=title,
                price=price,
            ).save()

        print(f'product {p}')

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')
        print(soup.prettify())

        container = soup.select('a.pagination-page')
        if not container:
            return 1
        last_button = container[-1]
        href = last_button.get('href')
        if not href:
            return 1

        r = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(r.query)
        return int(params['p'][0])

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # Запрос CSS-селектора, состоящего из множества классов, производится через select
        container = soup.select('div.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
        for item in container:
            self.parse_block(item=item)

    def parse_all(self):
        limit = self.get_pagination_limit()
        print(f'Всего страниц: {limit}')

        for i in range(1, limit + 1):
            self.get_blocks(page=i)
            # break


class Command(BaseCommand):
    help = 'Парсинг e-katalog'

    def handle(self, *args, **options):
        p = KatalogParser()
        p.parse_all()
