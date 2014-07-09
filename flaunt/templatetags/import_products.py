from cartridge.shop.models import Product
from mezzanine import template
register = template.Library()

@register.as_tag
def get_all_products():
    return Product.objects.all()



