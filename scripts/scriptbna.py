from decimal import Decimal

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from django.utils.timezone import make_aware
from webscrapping.models import Dollar, Type


def run():
    url = 'https://www.bna.com.ar/Personas'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for row in soup.find('table', {"class": "table cotizacion"}).tbody.findAll('tr'):
        origin = row.findAll('td')[0].text
        if (origin == 'Dolar U.S.A'):
            buy_price = row.findAll('td')[1].text
            sell_price = row.findAll('td')[2].text
            print(buy_price)
            print(sell_price)
            print(origin)
            dollar = Dollar(
                dollar_type=Type.objects.get(name="Oficial"),
                buy_price=Decimal(buy_price.replace(',', '.')),
                sell_price=Decimal(sell_price.replace(',', '.')),
                origin="Banco Nación",
                issue_date=make_aware(datetime.now()),
            )
            dollar.save()
            break
