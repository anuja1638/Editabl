from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import signup_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def homePageView(request):
    return render(request, template_name='homepage/homePage.html', context={})

def userProfileView(request):
    return render(request, template_name='userProfile/userProfile.html', context={})

def signUpPageView(request):
    if request.method == "POST":
        user_form = signup_form(request.POST)
        print('got it')
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            print('Registered')
            return HttpResponseRedirect('/')
    else:
        user_form = signup_form()
    return render(request, 'authentication/signUpPage.html', context={'user_form': user_form})


def user_exist_check(request):
    username = request.POST['username']
    username = username.strip()
    try:
        User.objects.get(username=username)
        status = 1
    except User.DoesNotExist:
        status = 0
    return JsonResponse({'status': status})


def loginPageView(request):
    if request.method == "POST":
        print("login_got")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            print('logged in')
        return HttpResponseRedirect('/')
    return render(request, 'authentication/loginPage.html', context={})


def authentication_check(request):
    username = request.POST['user_nm']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print(user)
    if user:
        status = 1
    else:
        status = 0
    return JsonResponse({'status': status})

@login_required(login_url='/login')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')