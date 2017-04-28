from django import forms

class SearchForm(forms.Form):
	search_field = forms.CharField(label='Search', max_length=1000, widget=forms.TextInput(attrs={'id': 'search-box'}))
