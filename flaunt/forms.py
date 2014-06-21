from django import forms
from models import Countrylist

class CountryForm(forms.Form):
	COUNTRY_CHOICES = [('','Please select a country'), ] + [(ctry.country, ctry.country) for ctry in Countrylist.objects.all()]
	CARRIER_CHOICES = [('','Please select a country first')]
	CARRIER_TYPES   = [('','Please select a country first')]
	country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'onchange':'getCountry(this);'}))
	shipping_type = forms.ChoiceField(choices=CARRIER_TYPES, widget=forms.Select(attrs={'onchange':'setCarriers(this);'}))
	carrier = forms.ChoiceField(choices=CARRIER_CHOICES, widget=forms.Select(attrs={'onchange':'getCarrier(this);'}))
