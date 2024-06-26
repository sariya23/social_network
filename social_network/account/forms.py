from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', "email")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def clean_password2(self):
        data = self.cleaned_data
        if data["password1"] != data["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return data["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже есть")
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"]

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже есть")
        return email


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")