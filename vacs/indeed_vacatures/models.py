import datetime

from django.db import models

class JobPost(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    titel = models.CharField(max_length=350, default="")
    bedrijf = models.CharField(max_length=350, default="")
    plaats = models.CharField(max_length=350, default="")
    link = models.CharField(max_length=350,default="")
    alles = models.CharField(max_length=50000,default="")

    def __str__(self):
        return self.titel