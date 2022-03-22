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
    path('userExistCheckUrl/', views.userExistCheckUrl, name='userExistCheckUrl'),
    path('authenticationCheck/', views.authenticationCheck, name='authenticationCheck'),
     path('editor/', views.manualEditingPageView, name='manualEditingPageUrl'),
]