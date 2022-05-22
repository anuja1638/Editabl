from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'AIAssistedEditing'

urlpatterns = [
    path('', views.AIEditingView, name='AIEditingPageUrl'),
    path('asyncProcess/', views.processImageAsync, name='processImage')
]