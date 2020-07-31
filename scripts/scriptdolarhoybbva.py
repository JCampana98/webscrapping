from decimal import Decimal

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.utils.timezone import make_aware
from webscrapping.models import Dollar, Type


def run():
    url = 'https://dolarhoy.com/cotizaciondolaroficial'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        buy_price = row.findAll('td')[1].text
        buy_price = buy_price[2: 7]
        sell_price = row.findAll('td')[2].text
        sell_price = sell_price[2: 7]
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
        if "Banco Frances" in origin:
            dollar.save()
            break
