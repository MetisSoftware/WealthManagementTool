from django.db import models


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()

    def __str__(self):  # __unicode__ if using python 2
        return self.first_name
