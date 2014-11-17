from django.db import models
from django.forms import ModelForm

# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    mob_phone = models.SmallIntegerField(max_length=11)
    home_phone = models.SmallIntegerField(max_length=11)
    dob = models.DateField()
    ni_number = models.CharField(max_length=8)

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'middle_name', 'surname', 'email', 'mob_phone', 'home_phone', 'dob', 'ni_number']
