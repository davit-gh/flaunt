from django import forms
from models import Countrylist, Carrierlist

class CountryForm(forms.Form):
	COUNTRY_CHOICES = [('','Please select a country'), ] + [(ctry.country, ctry.country) for ctry in Countrylist.objects.all()]
	CARRIER_CHOICES = [('','Please select a country first')]
	
	country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'onchange':'getCarriers(this);'}))
	carrier = forms.ChoiceField(choices=CARRIER_CHOICES)
