from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


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


class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email
