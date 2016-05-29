from mezzanine import template
import pdb
from cartridge.shop.models import Cart

register = template.Library()

@register.as_tag
def get_cart_object(request):
    cart = Cart.objects.from_request(request)
    if request.session.has_key('discount'):
        discount = cart.calculate_discount(request.session['discount'])
    else:
    	discount = 0
    #pdb.set_trace()
    return {'cart':cart, 'discount':discount}
