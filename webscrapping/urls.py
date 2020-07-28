from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from webscrapping.views import home_view, signup_view

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name="signup"),
    path('', home_view, name="home"),
]
