from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.gis import admin as geoadmin
from django.core.exceptions import ValidationError

from .models import Conversation, Item, ItemImage, Message


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'is_admin',
            'description'
        )


geoadmin.site.register(get_user_model())
geoadmin.site.unregister(Group)


class ItemAdmin(geoadmin.OSMGeoAdmin):
    list_display = ("name", "location", "description", "type", "user")


geoadmin.site.register(Item)
geoadmin.site.register(ItemImage)
geoadmin.site.register(Conversation)
geoadmin.site.register(Message)
