from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import cv2

# Create your views here.


@login_required(login_url = '/login')
def manualEditingPageView(request):
    return render(request, template_name='manualEditing/manualEditingPage.html')
