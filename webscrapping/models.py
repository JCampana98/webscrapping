from django.db import models


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
        ordering = ["issue_date"]
        verbose_name = "dólar"
        verbose_name_plural = "dólares"
        unique_together = ('issue_date', 'origin')


class Request(models.Model):
    value = models.DecimalField(verbose_name="valor", decimal_places=2, max_digits=30)
    mail = models.EmailField(verbose_name="mail")
    notified = models.BooleanField(verbose_name="notificado", default=False)

    class Meta:
        verbose_name = "petición"
        verbose_name_plural = "peticiones"
