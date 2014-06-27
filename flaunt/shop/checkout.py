from cartridge.shop.utils import set_shipping
from mezzanine.conf import settings
def billship_handler(request, order_form):
    
    if not request.session.get("free_shipping"):
        pass
