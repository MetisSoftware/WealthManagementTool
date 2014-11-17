from django.forms import ModelForm

from wms import models as m


class ClientForm(ModelForm):
    class Meta:
        model = m.Client
        fields = '__all__'
