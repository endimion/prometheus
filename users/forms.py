from django import forms

class RegisterForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_password = forms.CharField(label='Your password', max_length = 100)

class LoginForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length= 100)
    user_pass = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
