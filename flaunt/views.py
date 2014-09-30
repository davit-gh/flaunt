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
		carriers_priority=[cp[0] + '  '+cp[1]+' days '+'$'+cp[2] for cp in carriers_priority]
		
		#carriers_regular = map(lambda x: x.carrier, countrylist_country.carrierlistregular_set.all())
		#carriers_regular=[c_p[1:-1].split(', ') for c_p in carriers_regular]
		#carriers_regular=[cp[0] + '  '+cp[1]+' days '+'$'+cp[2] for cp in carriers_regular]
	else:
		carriers = "not ajax"
	#return render(request,'shop/cart.html',json.dumps({'carriers_priority':carriers_priority, 'carriers_regular':carriers_regular}), content_type="application/json")
	return HttpResponse(json.dumps({'carriers_priority':carriers_priority}), mimetype="application/json")

from cartridge.shop.forms import DiscountForm
def get_discount_on_update(request, discount_form_class=DiscountForm):
	discount_form = discount_form_class(request, request.POST or None)
	valid = discount_form.is_valid()
        if valid:
		discount_form.set_discount()
		recalculate_cart(request)
		discount_total = float("{0:.2f}".format(float(request.session.get('discount_total','0.00'))))
	else:
		discount_total = 0
	
 	return discount_total


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
			subtotal = float(cart.total_price())
			discount = get_discount_on_update(request)
			grand = "{0:.2f}".format(subtotal - discount)
			total_qty = int(cart.total_quantity())

			return HttpResponse(json.dumps({'sub':sub, 'subtotal' : subtotal, 'grand':grand, 'total_qty':total_qty, 'discount_total':discount}), content_type='application/json')
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
		if not request.POST.get("free_shipping"):
			carrier = request.POST['carrier']
			shipping_type = request.POST['shipping_type']
			shipping_total = float(carrier.split()[3][1:])
			settings.use_editable()
			set_shipping(request, shipping_type, shipping_total)
			recalculate_cart(request)
		else:
			shipping_type = 'Regular'
			shipping_total = 0.0
			set_shipping(request, shipping_type, shipping_total)
		
		subtotal = float(request.cart.total_price())
		discount = float(request.session.get('discount_total','0.00'))
		total = subtotal - discount + shipping_total
		total = "{0:.2f}".format(total)

		#resp = render_to_string('shop/cart.html', { 'request': request })
	return HttpResponse(json.dumps({'shipping_type' : shipping_type, 
									'shipping_total' : shipping_total, 
									'total_price' : total,
									'discount':discount,
									'subtotal':subtotal}), content_type='application/json')

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
			messages.info(request, _("Your feedback is saved. Thank you!"))
            		return redirect('shop_order_history')
		else:
			return HttpResponse('error')
			
    	# if a GET (or any other method) we'll create a blank form
    	else:
        	form = FeedbackForm()
	
	return render(request,'shop/includes/feedback.html',{'form':form, 'product_id':product_id})

from cartridge.shop.models import Cart, Order, ProductVariation, DiscountCode
def remove_cart(cart_pk,session, s_key):
	try:
            cart = Cart.objects.get(id=cart_pk)
            try:
                order = Order.objects.get(key=s_key)
                for field in order.session_fields:
                    if field in session:
                        del session[field]
                try:
                    del session["order"]
                except KeyError:
                    pass

                # Since we're manually changing session data outside of
                # a normal request, need to force the session object to
                # save after modifying its data.
                session.save()

                for item in cart:
                    try:
                        variation = ProductVariation.objects.get(
                            sku=item.sku)
                    except ProductVariation.DoesNotExist:
                        pass
                    else:
                        variation.update_stock(item.quantity * -1)
                        variation.product.actions.purchased()

                code = session.get('discount_code')
                if code:
                    DiscountCode.objects.active().filter(code=code) \
                        .update(uses_remaining=F('uses_remaining') - 1)
                cart.delete()
            except Order.DoesNotExist:
                pass
        except Cart.DoesNotExist:
            pass
	return session
            

from importlib import import_module
from flaunt.models import Btcinvoices, Pendingbtcinvoices
def blockchain_callback(request):
	SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
	if request.method == 'GET':
		query = request.GET
		address = query['address']
		secret = query['secret']
		confirmations = int(query['confirmations'])
		invoice_key = query['invoice_key']
		transaction_hash = query['transaction_hash']
		value_in_btc = str(float(query['value']) / 100000000)
		if request.GET.get('test'):
                        return HttpResponse('no tests now!')
		if address != settings.MY_BTC_ADDRESS:
			return HttpResponse('Incorrect Receiving Address')
		if secret != settings.BTC_SECRET:
			return HttpResponse('Invalid Secret')
		if confirmations >= 4:
			invoice, created = Btcinvoices.objects.get_or_create(invoice_key=invoice_key, transaction_hash=transaction_hash, value_in_btc=value_in_btc)
			if created:
				Pendingbtcinvoices.objects.get(invoice_key=invoice_key).delete()
			return HttpResponse("*ok*")
			
		else:
			pending, created = Pendingbtcinvoices.objects.get_or_create(invoice_key=invoice_key, transaction_hash=transaction_hash, value_in_btc=value_in_btc)
			sess = SessionStore(invoice_key)
			cpk = query['cart_pk']
			request.session = remove_cart(cpk, sess, invoice_key)
			return HttpResponse()

def check_request(request):
	if request.method == 'POST' and request.is_ajax():
		if request.session.get('order',False):
			return HttpResponse(json.dumps({'responsito' : "We didn't receive any confirmation yet. It may take about 2 mins for the payment to propagate in the blockchain. Please try again then."}), content_type='application/json')
		else:
			request.session["btc"] = "Thank you for your order. We will ship it after we receive at least 4 confirmations from bloc."
			return HttpResponse(json.dumps({'responsito' : "redirect"}), content_type='application/json')

# `data` is a python dictionary
def render_to_json(data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype="application/json")

from cartridge.shop.forms import AddProductForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext as _
from mezzanine.utils.views import set_cookie
from django.template.loader import render_to_string
from django.template import RequestContext
def handle_wishlist(request, slug, form_class=AddProductForm):
	if request.method == 'POST' and request.is_ajax():
		published_products = Product.objects.published(for_user=request.user)
		product = get_object_or_404(published_products, slug=slug)
		initial_data = {}
		variations = product.variations.all()
		fields = [f.name for f in ProductVariation.option_fields()]
		if variations:
			initial_data = dict([(f, getattr(variations[0], f)) for f in fields])
		initial_data["quantity"] = 1
		add_product_form = form_class(request.POST or None, product=product, initial=initial_data, to_cart=False)
		
		if add_product_form.is_valid():
			skus = request.wishlist
			
			sku = add_product_form.variation.sku
			if sku not in skus:
				skus.append(sku)
			messages.info(request, _("Item added to wishlist"))
			response = render(request,'messages.html')
			set_cookie(response, "wishlist", ",".join(skus))
			return response
		return HttpResponse(json.dumps(add_product_form.errors), mimetype="application/json")
	return HttpResponse('not post')

from django.contrib import messages
def remove_wishlist_item(request):
	if request.method == 'POST':
		skus = request.wishlist
		sku = request.POST.get("sku")
        if sku in skus:
        	skus.remove(sku)
        	message = _("Item removed from wishlist")
        	messages.info(request, message)
        response = render(request,'messages.html')
        set_cookie(response, "wishlist", ",".join(skus))
        return response

from flaunt.models import Inboundmail
from postmark_inbound import PostmarkInbound
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def mail_from_postmark(request):
        if request.method == 'POST':
                json_data = request.body
                body = json.loads(json_data)['HtmlBody']
                inbound = PostmarkInbound(json=json_data)
                mail = Inboundmail(html_body=inbound.text_body(), send_date=inbound.send_date(), subject=inbound.subject(), reply_to=inbound.reply_to(), sender=inbound.sender())
                mail.save()
                return HttpResponse('OK')
        else:
                return HttpResponse('not OK')

from cartridge.shop.models import Category
def get_category_products(request):
	if request.method == 'POST' and request.is_ajax():

		category = Category.objects.get(title=request.POST.get('cat'))
		products = category.products.all()
		#prods = [{"prods_on_sale": {"id": x.id, "title": x.title.strip(), "image": x.image, "unit_price": float(x.unit_price), "price": float(x.price()), "url": x.get_absolute_url()}} if x.on_sale() else {"prods":{"id": x.id, "title":x.title.strip(), "image": x.image, "price": float(x.price()), "url": x.get_absolute_url()}} for x in products]
		
		prods = [(x.id, x.title.strip(), x.image, float(x.unit_price), float(x.price()), x.get_absolute_url()) for x in products]
		
		return HttpResponse(json.dumps({'prods':zip(*prods)}), mimetype="application/json")
	return HttpResponse('Not OK!')


def get_discount(request, discount_form_class=DiscountForm):
	if request.method == 'POST' and request.is_ajax():
		discount_form = discount_form_class(request, request.POST or None)
		ship_type = request.session.get('shipping_type','Shipping fee:')
		ship_total = request.session.get('shipping_total','0.00')
		valid = discount_form.is_valid()
        if valid:
        	discount_form.set_discount()
        	recalculate_cart(request)
        	discount_total = float(request.session.get('discount_total',0))
		return HttpResponse(json.dumps({'discount_total': "{0:.2f}".format(discount_total), 'cart_total':float(request.cart.total_price()),'shipping_total':ship_total, 'shipping_type':ship_type}), mimetype="application/json")
        else:
        	return HttpResponse(json.dumps(discount_form.errors), mimetype="application/json")
		
