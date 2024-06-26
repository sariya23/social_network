from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', "email")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    def clean_password2(self):
        data = self.cleaned_data
        if data["password1"] != data["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return data["password2"]

