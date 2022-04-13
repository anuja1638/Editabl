from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'feed'
urlpatterns = [
    path('feed/', views.feedPageView, name='feedPageUrl'),
]