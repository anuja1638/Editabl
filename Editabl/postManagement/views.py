from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from .models import Post, DataURI
import datetime
import os
from Editabl.settings import MEDIA_ROOT

# Create your views here.

def dataURIToImg(uri):
    encodedData = uri.split(',')[1]
    decodedData = base64.b64decode(encodedData)
    img = Image.open(BytesIO(decodedData))
    return img


def addPostView(request, dataURIID):
    if request.method == "POST":
        dataURIObj = DataURI.objects.get(id=dataURIID)
        caption = request.POST['caption']
        postImg = dataURIToImg(dataURIObj.imageURI)
        dataURIObj.delete()
        currTime = datetime.datetime.now()
        currTimeStr = datetime.datetime.strftime(currTime, "%m-%d-%Y, %H:%M:%S")
        imgAbsPath = os.path.join(MEDIA_ROOT, 'posts',
                                str(request.user.id) + ' '+
                                currTimeStr + '.png')
        imgRelPath = os.path.join('posts',
                                str(request.user.id) + ' '+
                                currTimeStr + '.png')
        postImg.save(imgAbsPath)
        newPost = Post(user=request.user,
                    uploadTime=datetime.datetime.now(),
                    caption=caption)
        newPost.post = imgRelPath
        newPost.save()
        return JsonResponse({'status': 1})
    else:
        imgURIObj = DataURI.objects.get(id=int(dataURIID))
        imageURI = imgURIObj.imageURI
        return render(request, template_name='userProfile/addPostPage.html', context={'dataURI': imageURI, 'dataURIID': dataURIID})


def uploadPost(request):
    if request.method == "POST":
        dataURI = request.POST['dataURIString']
        dataURIObj = DataURI(imageURI=dataURI)
        dataURIObj.save()
        idURI = dataURIObj.id
        return JsonResponse({'status': 1, 'idURI': idURI})
