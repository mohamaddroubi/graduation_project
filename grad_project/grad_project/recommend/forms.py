from django import forms
from .models import Item
from django.db.models.fields import BLANK_CHOICE_DASH


class SearchForm(forms.Form):

	byBrand = forms.ChoiceField(
		label='Find by brand',
		choices=BLANK_CHOICE_DASH + list(Item.BRANDS), 
		required=False, 
		widget=forms.Select(attrs={'placeholder': 'Brand', 'required': False}),
		#null=True,
		#blank=True
		)

	byCat = forms.ChoiceField(
		label='Find by category', 
		choices=BLANK_CHOICE_DASH + list(Item.CATEGORIES), 
		required=False, 
		widget=forms.Select(attrs={'placeholder': 'Category', 'required': False}),
		#null=True,
		#blank=True
		)

