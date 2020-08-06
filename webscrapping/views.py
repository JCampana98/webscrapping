from django.contrib.auth import login, authenticate
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from datetime import timedelta
from statistics import mean

from .forms import SignUpForm, RequestForm
from django.shortcuts import render, redirect

from webscrapping.models import Dollar, Request


def home_view(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            petition = Request()
            petition.mail = form.cleaned_data['mail']
            petition.value = form.cleaned_data['value']
            petition.save()

            return redirect('home')
    else:
        form = RequestForm()
        today = make_aware(datetime.today())
        yesterday = today - timedelta(days=1)
        dollars = Dollar.objects.all()
        today_dollars = Dollar.objects.filter(issue_date__day=today.day,
                                              issue_date__month=today.month,
                                              issue_date__year=today.year)
        yesterday_dollars = Dollar.objects.filter(issue_date__day=yesterday.day,
                                                  issue_date__month=yesterday.month,
                                                  issue_date__year=yesterday.year)

        if not today_dollars:
            return render(request, 'home.html', {'today_dollars': yesterday_dollars,
                                                 'dollars': dollars,
                                                 'mean': mean(yesterday_dollars.values_list('sell_price', flat=True).values()),
                                                 'min': min(yesterday_dollars.values_list('sell_price', flat=True)),
                                                 'max': max(yesterday_dollars.values_list('sell_price', flat=True)),
                                                 'message': 'Todavía no hay información '
                                                            'disponible del dólar del dia de hoy.', 'form': form})
        elif not today_dollars and not yesterday_dollars:
            return render(request, 'home.html', {'message': 'No hay información reciente sobre el dolar',
                                                 'not_available': '', 'form': form})
        else:
            return render(request, 'home.html', {'today_dollars': today_dollars,
                                                 'dollars': dollars,
                                                 'form': form,
                                                 'mean': mean(today_dollars.values_list('sell_price', flat=True)),
                                                 'min': min(today_dollars.values_list('sell_price', flat=True)),
                                                 'max': max(today_dollars.values_list('sell_price', flat=True))})


def signup_view(request):
    form = SignUpForm(data=request.POST)

    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm(data=request.POST)
        print(form.errors)

    return render(request, 'signup.html', {'form': form})
