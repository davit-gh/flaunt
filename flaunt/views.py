from django.shortcuts import render
from flaunt.models import Countrylist
from django.http import HttpResponse
import json
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
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
	return HttpResponse(json.dumps({'carriers_priority':carriers_priority, 'carriers_regular':carriers_regular}), mimetype="application/json")

import pdb
from cartridge.shop.forms import CartItemFormSet
def update_cart(request):
	if request.is_ajax() and request.method == "POST":
		sub = {}
		grand = 0
		form = request.POST
		cart_formset = CartItemFormSet(request.POST, instance=request.cart)
		marked_for_delete = cart_formset.deleted_forms
		for form in cart_formset.forms:
			if form['id'].value() not in [deleted_record['id'].value() for deleted_record in marked_for_delete]:    
			    if form.is_valid():
				form.save()
				# save the form
			    else:
				pass
		valid = cart_formset.is_valid()
                if valid:
                    cart_formset.save()

		    for i in range(len(cart_formset)): 
			sub[i]=float(cart_formset[i].instance.total_price)
		    grand = float(cart_formset[0].instance.cart.total_price())
		    total_qty = int(cart_formset[0].instance.cart.total_quantity())
		else:
		    errors = cart_formset._errors
                    cart_formset = CartItemFormSet(instance=request.cart)
                    cart_formset._errors = errors
	
		return HttpResponse(json.dumps({'sub':sub, 'grand':grand, 'total_qty': total_qty}), content_type="application/json")
	else:
		return HttpResponse('not ok')
