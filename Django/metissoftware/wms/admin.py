from django.contrib import admin
from wms.models import Client, FA, Market, Share, Stock
from django import forms
from django.contrib.auth.admin import UserAdmin


class FACreationForm(forms.ModelForm):
    # For creating FAs
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = FA
        fields = ('first_name', 'surname', 'email', 'dob',
                  'ni_number', 'is_superuser', 'is_staff',
                  'is_admin', 'is_active'
                  )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Empty password")
        return password

    def save(self, commit=True):
        user = super(FACreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class FAChangeForm(forms.ModelForm):

    class Meta:
        model = FA
        fields = ('first_name', 'surname', 'email', 'dob',
                  'ni_number', 'is_superuser', 'is_staff',
                  'is_admin', 'is_active')

    def clean_password(self):
        return self.initial["password"]


class FAAdmin(UserAdmin):
    add_form = FACreationForm
    form = FAChangeForm

    list_display = ('email', 'dob', 'is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name', 'surname', 'ni_number', 'email',
                           'is_superuser', 'is_staff', 'is_admin',
                           'is_active', 'password')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'surname', 'ni_number',
                       'email', 'dob', 'is_staff',
                       'is_superuser', 'is_admin', 'password')
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(Client)
admin.site.register(FA, FAAdmin)
admin.site.register(Market)
admin.site.register(Share)
admin.site.register(Stock)
