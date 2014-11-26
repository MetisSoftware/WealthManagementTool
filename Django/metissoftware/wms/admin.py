from django.contrib import admin
from wms.models import Client
from wms.models import FA
from wms.models import FAtoClient

# Register your models here.
admin.site.register(Client)
admin.site.register(FA)
admin.site.register(FAtoClient)