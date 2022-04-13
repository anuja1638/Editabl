import email
from statistics import mode
from django.db import models

# Create your models here.

class abousUsModal(models.Model):
    name = models.CharField(max_length=512)
    email = models.EmailField()
    phone = models.IntegerField()
    message = models.TextField()