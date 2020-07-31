from django.contrib.auth import login, authenticate
from django.utils.datetime_safe import datetime

from .forms import SignUpForm
from django.shortcuts import render, redirect
from .models import Type, Dollar
from django.conf import settings
from django.utils.timezone import make_aware
import requests


def home_view(request):
    dollar_object_oficial = Dollar()
    dollar_object_oficial.scraping()



    today = make_aware(datetime.today())
    dollars = Dollar.objects.all()
    today_dollars = Dollar.objects.filter(issue_date__day=today.day,
                                          issue_date__month=today.month,
                                          issue_date__year=today.year)
    return render(request, 'home.html', {'today_dollars': today_dollars, 'dollars': dollars, 'dollar_object_oficial': dollar_object_oficial})


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
