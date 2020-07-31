from django.db import models
from django.utils.timezone import now
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import requests

class Type(models.Model):
    name = models.CharField(verbose_name="nombre del tipo de dólar", max_length=16, unique=True)

    class Meta:
        verbose_name = "tipo de dólar"
        verbose_name_plural = "tipos de dólar"

    def __str__(self):
        return self.name


class Dollar(models.Model):
    dollar_type = models.ForeignKey(Type, verbose_name="tipo de dolar", on_delete=models.DO_NOTHING)
    buy_price = models.DecimalField(verbose_name="precio de compra", decimal_places=2, max_digits=30)
    sell_price = models.DecimalField(verbose_name="precio de venta", decimal_places=2, max_digits=30)
    issue_date = models.DateTimeField(verbose_name="fecha y hora")
    origin = models.CharField(verbose_name="origen del precio", max_length=200)

    class Meta:
        verbose_name = "dólar"
        verbose_name_plural = "dólares"
        unique_together = ('issue_date', 'origin')

    def scraping(self):
        url = 'https://drdolar.com/cotizaciones/bancos'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for row in soup.findAll('table')[6].tbody.findAll('tr'):
            self.buy_price = row.findAll('td')[1].text
            self.buy_price = self.buy_price[1: 6]
            self.sell_price = row.findAll('td')[3].text[0:6]
            self.sell_price = self.sell_price[1: 6]
            self.dollar_type = Type.objects.get(name="oficial")
            self.origin = row.findAll('td')[0].text
            self.issue_date = datetime.now()

            event1 = Dollar(
                dollar_type=Type.objects.get(name="oficial"),
                buy_price=Decimal(self.buy_price.replace(',', '.')),
                sell_price=Decimal(self.sell_price.replace(',', '.')),
                origin = row.findAll('td')[0].text,
                issue_date=datetime.now(),
            )
            event1.save()


class Request(models.Model):
    value = models.DecimalField(verbose_name="valor", decimal_places=2, max_digits=30)
    mail = models.EmailField(verbose_name="mail")
    notified = models.BooleanField(verbose_name="notificado", default="false")

    class Meta:
        verbose_name = "petición"
        verbose_name_plural = "peticiones"
