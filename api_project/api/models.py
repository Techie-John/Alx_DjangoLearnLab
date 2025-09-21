from django.db import models

class Book(models.Model):
    title = models.charfield(max_length=500)
    author = models.charfield(max_length=500)
# Create your models here.
