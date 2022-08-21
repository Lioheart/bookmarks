from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Użytkownik')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
