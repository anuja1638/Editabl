from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.homePageView, name='homePageUrl'),
    path('login/', views.loginPageView, name='loginPageUrl'),
    path('signup/', views.signUpPageView, name='signUpPageUrl'),
    path('logout/', views.logoutView, name='logoutUrl'),
    path('user_profile/,', views.userProfileView, name='userProfileUrl' ),
    path('user_exist_check/', views.user_exist_check, name='user_exist_check_url'),
    path('authentication_check/', views.authentication_check, name='authentication_check'),
]