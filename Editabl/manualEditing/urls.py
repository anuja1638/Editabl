from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'manualEditing'

urlpatterns = [
   path('editor/', views.manualEditingPageView, name='manualEditingPageUrl')
    ]