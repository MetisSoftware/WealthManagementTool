from django.db import models
from django.forms import ModelForm


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=64,default="**DEFAULT**")
    middle_name = models.CharField(max_length=64,null=True)
    surname = models.CharField(max_length=64,default="**DEFAULT**")
    email = models.EmailField(max_length=64,default="**DEFAULT**")
    mob_phone = models.SmallIntegerField(max_length=11,null=True)
    home_phone = models.SmallIntegerField(max_length=11,null=True)
    dob = models.DateField(default="1990-01-01")
    ni_number = models.CharField(max_length=8,default="DEFAULT")

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'middle_name', 'surname', 'email', 'mob_phone', 'home_phone', 'dob', 'ni_number']

    def __str__(self):  # __unicode__ if using python 2
        return self.first_name

