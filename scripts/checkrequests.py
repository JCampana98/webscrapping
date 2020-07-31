from django.core.mail import EmailMessage
from webscrapping.models import Dollar, Request
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware


def run():
    today = make_aware(datetime.today())
    today_dollars = Dollar.objects.filter(issue_date__day=today.day,
                                          issue_date__month=today.month,
                                          issue_date__year=today.year)
    requests = Request.objects.all()
    for dollar in today_dollars:
        for request in requests:
            if dollar.sell_price > request.value and not request.notified:
                msg = EmailMessage('Aviso de Cambio del Dolar',
                                   'Estimado usario, se le notifica por el '
                                   'presente mail que el valor del dolar para su venta'
                                   ' ha superado los: $' + request.value.to_eng_string(),
                                   from_email='from@example.com',
                                   to=[request.mail])
                request.__setattr__('notified', True)
                request.save()
                msg.send()
