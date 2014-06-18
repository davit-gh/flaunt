from mezzanine import template
from suds.client import Client
from flaunt.forms import CountryForm
register = template.Library()

@register.as_tag
def get_countries(*args):
	url = 'http://www.sendfromchina.com/shipfee/web_service?wsdl'
	client = Client(url)
	countries = client.service.getCountries()
	countries = map(lambda x: x._enName, countries)
	return countries

@register.as_tag
def get_available_carriers(weight,country,length,width,height):
	url = 'http://www.sendfromchina.com/shipfee/web_service?wsdl'
	client = Client(url)
	rates = client.service.getRates(weight,country,length,width,height)
	rates=map(lambda x: (x._shiptypecode, x._totalfee), rates)
	return rates

@register.as_tag
def make_form(*args):
	return CountryForm()
