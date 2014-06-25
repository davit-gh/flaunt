from cartridge.shop.utils import set_shipping
from mezzanine.conf import settings
def billship_handler(request, shipping_type, shipping_total):
    
    if not request.session.get("free_shipping"):
        settings.use_editable()
        set_shipping(request, shipping_type, shipping_total)
