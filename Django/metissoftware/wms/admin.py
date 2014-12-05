from django.contrib import admin
from wms.models import Client, FA, Market,Share,Stock

# Register your models here.
admin.site.register(Client)
admin.site.register(FA)
admin.site.register(Market)
admin.site.register(Share)
admin.site.register(Stock)
