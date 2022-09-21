from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Item

User = get_user_model()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    def is_valid(self):
        return True

    class Meta:
        model = User
        fields = ("email", "password")

        def clean(self):
            if self.is_valid():

                email = self.cleaned_data('email')
                password = self.cleaned_data('password')

                if not authenticate(email=email, password=password):
                    raise forms.ValidationError("Invalid LOGIN")


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "item_type", "category1", "category2", "category3", "description"]
