from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class FormRegistrationUser(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirmation_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmation_password"]

    def clean(self):
        super().clean()
        password = self.cleaned_data["password"]
        confirmation_password = self.cleaned_data["confirmation_password"]
        if password != confirmation_password:
            raise forms.ValidationError("passwords do not match")
        return self.cleaned_data


