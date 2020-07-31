from decimal import Decimal

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.utils.timezone import make_aware
from webscrapping.models import Dollar, Type


def run():
    url = 'https://drdolar.com/cotizaciones/bancos'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for row in soup.findAll('table')[6].tbody.findAll('tr'):
        buy_price = row.findAll('td')[1].text
        buy_price = buy_price[1: 6]
        sell_price = row.findAll('td')[3].text[0:6]
        sell_price = sell_price[1: 6]
        origin = row.findAll('td')[0].text
        print(buy_price)
        print(sell_price)
        print(origin)
        dollar = Dollar(
            dollar_type=Type.objects.get(name="Oficial"),
            buy_price=Decimal(buy_price.replace(',', '.')),
            sell_price=Decimal(sell_price.replace(',', '.')),
            origin=origin,
            issue_date=make_aware(datetime.now()),
        )
        if "Brubank" in origin:
            dollar.save()
            break
