from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ImageField(upload_to='posts')
    uploadTime = models.DateTimeField()
    caption = models.TextField()

class DataURI(models.Model):
    imageURI = models.TextField()
