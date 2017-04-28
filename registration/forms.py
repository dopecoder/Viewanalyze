from django import forms
from passwords.fields import PasswordField

class RegistrationForm(forms.Form):
	first_name = forms.CharField(label='first name', max_length=30)
	#middle_name = forms.CharField(label='middle name', max_length=30, required=False)
	last_name = forms.CharField(label='last name', max_length=30)
	#username = forms.CharField(label='username', max_length=15)
	email = forms.EmailField()
	password = PasswordField(label='password')
	re_password = PasswordField(label='re-enter password')
	#password = forms.CharField(label='password', max_length=16, min_length=8, widget=forms.PasswordInput)
	#re_password = forms.CharField(label='re-enter password', max_length=16, min_length=8, widget=forms.PasswordInput)
	#dob = forms.DateField(label='date_of_birth',  input_formats=['%d/%m/%Y'])
	#country = forms.CharField(label='country', max_length=20)
	terms = forms.BooleanField(
    error_messages={'required': 'You must accept the terms and conditions'},
    label="Terms&Conditions"
	)
	#country = forms.ChoiceField(choices=CHOICES)


class MailForm(forms.Form):
	email = forms.EmailField(label='email')
