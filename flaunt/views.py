from django.shortcuts import render
from flaunt.models import Countrylist
from django.http import HttpResponse
from cartridge.shop.utils import set_shipping
from django.template.loader import render_to_string
from cartridge.shop.utils import recalculate_cart
import json
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
import pdb
@ensure_csrf_cookie
def ajax_country(request):
	if request.is_ajax() and request.method == 'POST':

		#message="is ajax"
		countrylist_country = Countrylist.objects.get(country=request.POST['country'])
		carriers_priority=map(lambda x: x.carrier,countrylist_country.carrierlistpriority_set.all())
		carriers_priority=[c_p[1:-1].split(', ') for c_p in carriers_priority]
		carriers_priority=[cp[0] + '  '+cp[1]+' days '+cp[2]+'Y' for cp in carriers_priority]
		
		carriers_regular = map(lambda x: x.carrier, countrylist_country.carrierlistregular_set.all())
		carriers_regular=[c_p[1:-1].split(', ') for c_p in carriers_regular]
		carriers_regular=[cp[0] + '  '+cp[1]+' days '+cp[2]+'Y' for cp in carriers_regular]
	else:
		carriers = "not ajax"
	#return render(request,'shop/cart.html',json.dumps({'carriers_priority':carriers_priority, 'carriers_regular':carriers_regular}), content_type="application/json")
	return HttpResponse(json.dumps({'carriers_priority':carriers_priority, 'carriers_regular':carriers_regular}), mimetype="application/json")


from cartridge.shop.forms import CartItemFormSet
def update_cart(request):
	if request.is_ajax() and request.method == "POST":
		sub = {}
		grand = 0
		form = request.POST
		shipping_type = request.POST['shipping_type'] if request.POST.get('shipping_type') else ''
		carrier = request.POST[shipping_type] if shipping_type is not '' else ''
		shipping_total = float(carrier.split()[3][:-1]) if carrier is not '' else 0
		cart_formset = CartItemFormSet(request.POST, instance=request.cart)
		cart = cart_formset[0].instance.cart

		valid = cart_formset.is_valid()
		if valid:
			cart_formset.save()
			for i in range(len(cart_formset)):
				sub[i]=float(cart_formset[i].instance.total_price)
			grand = float(cart.total_price()) 
			request.session['grand_total'] = grand + shipping_total
			total_qty = int(cart.total_quantity())
			return HttpResponse(json.dumps({'sub':sub, 'grand':grand, 'total_qty':total_qty}), content_type='application/json')
		else:
			errors = cart_formset._errors
			cart_formset = CartItemFormSet(instance=request.cart)
			cart_formset._errors = errors
			return HttpResponse(json.dumps({'errors' : errors}), content_type='application/json')
	else:
		return HttpResponse('Sth went wrong.')


def get_carrier(request):
	if request.is_ajax() and request.method == 'POST':
		carrier = request.POST['carrier']
		shipping_type = request.POST['shipping_type']
		shipping_total = float(carrier.split()[3][:-1])
		total = float(request.cart.total_price())
		if not request.session.get("free_shipping"):
			set_shipping(request, shipping_type, shipping_total)
		recalculate_cart(request)
		request.session['grand_total'] = shipping_total + total
		#resp = render_to_string('shop/cart.html', { 'request': request })
	return HttpResponse(json.dumps({'shipping_type' : shipping_type, 
									'shipping_total' : shipping_total, 
									'total_price' : total}), content_type='application/json')