from django import forms


class LoginForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length= 100)
    user_pass = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)



