from django.utils.translation import ugettext_lazy as _
from django import forms
from models import Countrylist
from django.forms import ModelForm, Textarea, TextInput
from flaunt.models import Feedback
import pdb
class CountryForm(forms.Form):
	COUNTRY_CHOICES = [('','Please select a country'), ] + [(ctry.country, ctry.country) for ctry in Countrylist.objects.all()]
	#CARRIER_TYPES = [('','Please select shipping type')]
	CARRIER_TYPES = [('','Please select the shipping type'), ('Regular', 'Regular Shipping (free)'), ('Priority Shipping', 'Priority Shipping')]
	CARRIER_CHOICES   = [('','Please select shipping type')]
	country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'onchange':'getCountry(this);'}))
	shipping_type = forms.ChoiceField(choices=CARRIER_TYPES, widget=forms.Select(attrs={'onchange':'setCarriers(this);'}))
	carrier = forms.ChoiceField(choices=CARRIER_CHOICES, widget=forms.Select(attrs={'onchange':'getCarrier(this);'}))
	
class FeedbackForm(ModelForm):
	class Meta:
		model = Feedback
		fields = ['item_title', 'feedback_text']
		widgets = {
			'item_title': TextInput(attrs={
				'class': 'form-control',
				'required': 'required'
			}),
			'feedback_text': Textarea(attrs={
				'placeholder':_('Thank you for your comment!'),
				'class': 'form-control',
				'required': 'required'
			}),
		}
