from django.contrib import admin
from flaunt.models import HomePage, Slide, Portfolio, AddFieldsToProducts, FAQ, FAQPage
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

class FAQAdmin(TabularDynamicInlineAdmin):
	model=FAQ

class FAQPageAdmin(PageAdmin):
	inlines = [FAQAdmin,]

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
product_fieldsets[0][1]["fields"] += ("short_desc", "additional")
ProductAdmin.fieldsets = product_fieldsets
#admin.site.unregister(Product)
#admin.site.register(Product, Product_with_short_desc)
#-----------------------------------------------------------------
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
#admin.site.register(Slide, SlideAdmin)
admin.site.register(HomePage,HomePageAdmin)
admin.site.register(FAQPage,FAQPageAdmin)
#admin.site.register(FAQ,PageAdmin)
admin.site.register(Portfolio,PageAdmin)
admin.site.register(PortfolioItem,PortfolioItemAdmin)
admin.site.register(PortfolioItemCategory)
#admin.site.register(Slide)

from flaunt.models import Feedback
admin.site.register(Feedback)

from flaunt.models import Inboundmail
from django.utils.html import format_html
class InboundmailAdmin(admin.ModelAdmin):
#        fields=('send_date', 'subject', 'html_body', 'reply_to', 'sender')
        list_display=('send_date', 'subject', 'html_body', 'reply_to', 'sender')

#        def format_as_html(self,obj):
#                return format_html(obj.html_body)
#        format_as_html.allow_tags = True
#        format_as_html.short_description = 'Body'
admin.site.register(Inboundmail, InboundmailAdmin)

from flaunt.models import Btcinvoices
from flaunt.models import Pendingbtcinvoices
class Btcinvoicesadmin(admin.ModelAdmin):
	list_display=('invoice_key','transaction_hash','value_in_btc')

class Pendingbtcinvoicesadmin(admin.ModelAdmin):
	list_display=('invoice_key','transaction_hash','value_in_btc')
admin.site.register(Btcinvoices,Btcinvoicesadmin)
admin.site.register(Pendingbtcinvoices,Pendingbtcinvoicesadmin)