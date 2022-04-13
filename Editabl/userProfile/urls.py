from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'userProfile'

urlpatterns = [
    path('',  views.userProfileView, name="userProfileUrl"),
    path('addPost/', views.addPostView, name = "addPostUrl")
]