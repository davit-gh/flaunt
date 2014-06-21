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

@register.filter(name='fee')
def get_shipping_fee(req):
	return req.session['shipping_total'] if req.session.get("shipping_total") else 0

@register.filter(name='type')
def get_shipping_type(req):
	return req.session['shipping_type'] if req.session.get('shipping_type') else ''

@register.filter
def remove_shipping_info(req, shipping_info):
	del req.session[shipping_info]
	return ''

@register.filter
def contains_shipping_info(req):
	return req.session.get("shipping_total")

@register.filter
def cart_total_price(req):
	return req.cart.total_price()
	
