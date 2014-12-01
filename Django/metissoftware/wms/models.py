from django.db import models
from django.forms import ModelForm


# Create your models here.


class FA(models.Model):
    first_name = models.CharField(max_length=64,default="**DEFAULT**")
    surname = models.CharField(max_length=64,default="**DEFAULT**")
    dob = models.DateField(default="1990-01-01")
    ni_number = models.CharField(max_length=9,default="DEFAULT", primary_key=True)
    email = models.EmailField(max_length=64,default="**DEFAULT**")
    mob_number = models.CharField(max_length=11,null=True)
    off_number = models.CharField(max_length=11,null=True)
    password = models.CharField(max_length=64,default="**DEFAULT**")

    def __str__(self):
        return self.surname+" - "+self.ni_number

class Client(models.Model):
    first_name = models.CharField(max_length=64,default="**DEFAULT**")
    middle_name = models.CharField(max_length=64,null=True)
    surname = models.CharField(max_length=64,default="**DEFAULT**")
    email = models.EmailField(max_length=64,default="**DEFAULT**")
    mob_phone = models.CharField(max_length=11,null=True)
    home_phone = models.CharField(max_length=11,null=True)
    dob = models.DateField(default="1990-01-01")
    ni_number = models.CharField(max_length=9,default="DEFAULT", primary_key=True)
    fa = models.ForeignKey(FA)
    def __str__(self):
        return self.surname+" - "+self.ni_number


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'middle_name', 'surname', 'email',
                  'mob_phone', 'home_phone', 'dob', 'ni_number', 'fa']

    def __str__(self):  # __unicode__ if using python 2
        return self.first_name

