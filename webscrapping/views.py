from django.contrib.auth import login, authenticate
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from datetime import timedelta

from .forms import SignUpForm
from django.shortcuts import render, redirect

from webscrapping.models import Dollar


def home_view(request):
    today = make_aware(datetime.today())
    yesterday = today - timedelta(days=1)
    dollars = Dollar.objects.all()
    today_dollars = Dollar.objects.filter(issue_date__day=today.day,
                                          issue_date__month=today.month,
                                          issue_date__year=today.year).order_by('issue_date')
    yesterday_dollars = Dollar.objects.filter(issue_date__day=yesterday.day,
                                              issue_date__month=yesterday.month,
                                              issue_date__year=yesterday.year).order_by('issue_date')

    if not today_dollars:
        return render(request, 'home.html', {'today_dollars': yesterday_dollars, 'dollars': dollars, 'message': 'Todavía no hay información disponible del dolar del dia de hoy'})
    elif not today_dollars and not yesterday_dollars:
        return render(request, 'home.html', {'message': 'today_dollars', 'not_available': ''})
    else:
        return render(request, 'home.html', {'today_dollars': today_dollars, 'dollars': dollars})


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
