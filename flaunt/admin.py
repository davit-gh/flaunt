from django.contrib import admin
from flaunt.models import HomePage, Slide, Portfolio, AddFieldsToProducts
from flaunt.models import PortfolioItem, PortfolioItemImage, PortfolioItemCategory
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from copy import deepcopy
from cartridge.shop.admin import ProductAdmin
from cartridge.shop.models import Product
#from cartridge.shop.forms import ProductAdminForm

class SlideAdmin(TabularDynamicInlineAdmin):
	model=Slide

class HomePageAdmin(PageAdmin):
	inlines = [SlideAdmin,]

class PortfolioItemImageInline(TabularDynamicInlineAdmin):
	model=PortfolioItemImage

class PortfolioItemAdmin(PageAdmin):
	inlines=(PortfolioItemImageInline, )

class AddFieldsToProductAdmin(TabularDynamicInlineAdmin):
	model = AddFieldsToProducts

class MyProductAdmin(ProductAdmin):
	inlines=(AddFieldsToProductAdmin, )


#re-registering Cartridge Products to add short_description to it
product_fieldsets = deepcopy(ProductAdmin.fieldsets)
product_fieldsets[0][1]["fields"] += ("short_descript",)

ProductAdmin.fieldsets = product_fieldsets
#admin.site.unregister(Product)
#admin.site.register(Product, Product_with_short_desc)
#-----------------------------------------------------------------
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.register(HomePage,HomePageAdmin)
admin.site.register(Portfolio,PageAdmin)
admin.site.register(PortfolioItem,PortfolioItemAdmin)
admin.site.register(PortfolioItemCategory)
#admin.site.register(Slide)


