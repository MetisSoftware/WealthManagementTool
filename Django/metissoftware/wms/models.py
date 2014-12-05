from django.db import models
from django.forms import ModelForm


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=64, default="**DEFAULT**")
    surname = models.CharField(max_length=64, default="**DEFAULT**")
    dob = models.DateField(default="1990-01-01")
    ni_number = models.CharField(max_length=9, default="DEFAULT", primary_key=True)
    email = models.EmailField(max_length=64, default="**DEFAULT**")

    class Meta:
        abstract = True


class FA(User):
    mob_number = models.CharField(max_length=11, null=True)
    off_number = models.CharField(max_length=11, null=True)
    password = models.CharField(max_length=64, default="**DEFAULT**")

    def __str__(self):
        return self.surname+" - "+self.ni_number


class Client(User):
    middle_name = models.CharField(max_length=64, null=True)
    home_phone = models.CharField(max_length=11, null=True)
    mob_phone = models.CharField(max_length=11, null=True)
    cash = models.DecimalField(max_digits=20,decimal_places=2)
    fa = models.ForeignKey(FA)

    def __str__(self):
        return self.surname+" - "+self.ni_number



class Market(models.Model):
    name = models.CharField(primary_key=True, max_length=10)
    full_name = models.CharField(max_length=64)

    def __str__(self):
        return  self.name

class Stock(models.Model):
    symbol = models.CharField(primary_key=True,max_length=5)
    company = models.CharField(max_length=64)
    market = models.ForeignKey(Market)

    def __str__(self):
        return self.symbol

class Share(models.Model):
    owner = models.ForeignKey(Client)
    buy_date = models.DateField(default = "1990-01-01")
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=20,decimal_places=2)
    stock = models.ForeignKey(Stock)

    def __str__(self):
        return self.owner.surname + " " + self.owner.ni_number+" - "+self.stock.symbol

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'middle_name', 'surname', 'email',
                  'mob_phone', 'home_phone', 'dob', 'ni_number', 'fa', 'cash']

    def __str__(self):
        return self.first_name
