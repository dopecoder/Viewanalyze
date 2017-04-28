from django import forms
from passwords.fields import PasswordField

class LoginForm(forms.Form):
	email = forms.EmailField(label='your email', max_length=100)
	password = forms.CharField(label='your password', max_length=16, widget=forms.PasswordInput)
	remember_me = forms.BooleanField(label='keep me logged in', required=False)

class PasswordResetForm(forms.Form):
	email = forms.EmailField(label='email')
	password = PasswordField(label='new password')
	re_password = PasswordField(label='re-enter new password')