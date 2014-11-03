from django.db import models

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()