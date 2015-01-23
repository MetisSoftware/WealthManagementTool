from django.contrib import admin
from wms.models import Client, FA, Market, Share, Stock
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class FACreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = FA
        fields = ('email', 'dob', 'first_name', 'surname',
                  'ni_number')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save password in hashed format for security
        user = super(FACreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            return user

class FAChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = FA
        fields = ('email', 'password', 'dob', 'is_active', 'is_admin',
                  'first_name', 'surname', 'ni_number')

        def clean_password(self):
            return self.initial["password"]

class FAAdmin(UserAdmin):
    # Add and change user instances
    form = FAChangeForm
    add_form = FACreationForm

    # Fields used displaying user model
    # override useradmin
    list_display = ('email', 'dob', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'dob', 'password',
                           'first_name', 'surname', 'ni_number'
                           )}),
        ('Personal info', {'fields': ('dob',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dob', 'password1',
                       'password2', 'first_name', 'surname',
                       'ni_number')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Register the new UserAdmin
#admin.site.register(FA, MyUserAdmin)
# overriding Django's built in permissions
admin.site.unregister(Group)



# Register your models here.
admin.site.register(Client)
admin.site.register(FA, FAAdmin)
admin.site.register(Market)
admin.site.register(Share)
admin.site.register(Stock)
