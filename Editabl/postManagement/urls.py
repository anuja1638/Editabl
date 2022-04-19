from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'postManagement'

urlpatterns = [
   path('uploadPost/>', views.uploadPost, name='uploadPostUrl'),
   path('addPost/<str:dataURIID>', views.addPostView, name = "addPostUrl")
    ]