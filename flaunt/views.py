from django.shortcuts import render
from django.shortcuts import redirect
from flaunt.models import Countrylist
from django.http import HttpResponse
from cartridge.shop.utils import set_shipping
from django.template.loader import render_to_string
from cartridge.shop.utils import recalculate_cart
from mezzanine.conf import settings
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
		
		cart_formset = CartItemFormSet(request.POST, instance=request.cart)
		cart = cart_formset[0].instance.cart

		valid = cart_formset.is_valid()
		if valid:
			cart_formset.save()
			sub = [float(f.instance.total_price) for f in cart_formset]
			grand = float(cart.total_price()) 
			
			total_qty = int(cart.total_quantity())
			return HttpResponse(json.dumps({'sub':sub, 'grand':grand, 'total_qty':total_qty}), content_type='application/json')
		else:
			errors = cart_formset._errors
			cart_formset = CartItemFormSet(instance=request.cart)
			cart_formset._errors = errors
			return HttpResponse(json.dumps({'errors' : errors}), content_type='application/json')
	else:
		return HttpResponse('Sth went wrong.')

from flaunt.shop.checkout import billship_handler
def get_carrier(request):
	if request.is_ajax() and request.method == 'POST':
		carrier = request.POST['carrier']
		shipping_type = request.POST['shipping_type']
		shipping_total = float(carrier.split()[3][:-1])
		total = float(request.cart.total_price())
		if not request.session.get("free_shipping"):
			settings.use_editable()
			set_shipping(request, shipping_type, shipping_total)
		
		recalculate_cart(request)
		
		#resp = render_to_string('shop/cart.html', { 'request': request })
	return HttpResponse(json.dumps({'shipping_type' : shipping_type, 
									'shipping_total' : shipping_total, 
									'total_price' : total}), content_type='application/json')
import pdb
from flaunt.forms import FeedbackForm
from flaunt.models import Feedback
from flaunt.models import Product
from django.core.urlresolvers import reverse
def save_feedback(request, product_id):
	if request.method == 'POST':
        # create a form instance and populate it with data from the request:
		product = Product.objects.get(id=product_id)
		fb = Feedback(product=product, user=request.user)
        	form = FeedbackForm(request.POST,instance=fb)
        # check whether it's valid:
        	if form.is_valid():
            	# process the data in form.cleaned_data as required
            		form.save()
            	# redirect to a new URL:
            		return redirect('shop_order_history')
		else:
			return HttpResponse('error')
			
    	# if a GET (or any other method) we'll create a blank form
    	else:
        	form = FeedbackForm()
	
	return render(request,'shop/includes/feedback.html',{'form':form, 'product_id':product_id})

from flaunt,models import Btcinvoices, Pendingbtcinvoices
def blockchain_callback(request):
	if request.method == 'GET':
		query = request.GET
		address = query['address']
		secret = query['secret']
		confirmations = int(query['confirmations'])
		invoice_key = query['invoice_key']
		transaction_hash = query['transaction_hash']
		value_in_btc = query['value']
		if address != settings.MY_BTC_ADDRESS:
			return HttpResponse('Incorrect Receiving Address')
		if secret != settings.BTC_SECTRET:
			return HttpResponse('Invalid Secret')
		if confirmations >= 4:
			invoice created = Btcinvoices.objects.get_or_create(invoice_key, transaction_hash, value_in_btc)
			if created:
				Pendingbtcinvoices.objects.get(invoice_key=invoice_key).delete()
			return HttpResponse("*ok*")
			
		else:
			pending created = Pendingbtcinvoices.objects.get_or_create(invoice_key, transaction_hash, value_in_btc)
			
			return HttpResponse("Waiting for more confirmations.")