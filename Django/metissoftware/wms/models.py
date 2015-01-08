from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=64, default="**DEFAULT**")
    surname = models.CharField(max_length=64, default="**DEFAULT**")
    dob = models.DateField(default="1990-01-01")
    ni_regex = RegexValidator(regex=r'^(?!BG)(?!GB)(?!NK)(?!KN)(?!TN)(?!NT)(?!ZZ)(?:[A-CEGHJ-PR-TW-Z][A-CEGHJ-NPR-TW-Z])(?:\s*\d\s*){6}([A-D]|\s)$', message="Must be in the format: 'AA999999A', restrictions to characters apply'")
    ni_number = models.CharField(max_length=9, validators=[ni_regex], primary_key=True)
    #ni_number = models.CharField(max_length=9, default="DEFAULT", primary_key=True)
    email = models.EmailField(max_length=64, default="**DEFAULT**")

    class Meta:
        abstract = True


class FA(User):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Must be entered in the format: '+999999999'.")
    mob_number = models.CharField(validators=[phone_regex], max_length=9, null=True)
    off_number = models.CharField(validators=[phone_regex], max_length=9, null=True)
    password = models.CharField(max_length=64, default="**DEFAULT**")

    def __str__(self):
        return self.surname+" - "+self.ni_number


class Client(User):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 9 digits allowed.")
    middle_name = models.CharField(max_length=64, null=True)
    home_phone = models.CharField(max_length=11, validators=[phone_regex], blank=True)
    mob_phone = models.CharField(max_length=11, validators=[phone_regex], blank=True)
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
