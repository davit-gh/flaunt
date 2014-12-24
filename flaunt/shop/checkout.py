from cartridge.shop.utils import set_shipping
from mezzanine.conf import settings
from django.utils.translation import ugettext as _

def billship_handler(request, order_form):
    
    if not request.session.get("free_shipping"):
        pass

