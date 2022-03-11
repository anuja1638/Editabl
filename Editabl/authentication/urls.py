from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.homePageView, name='homePageUrl')
]