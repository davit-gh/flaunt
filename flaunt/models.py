from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to
from mezzanine.core.models import Displayable
from cartridge.shop.models import Product


from importlib import import_module

from mezzanine.conf import settings

from cartridge.shop.models import Cart, Order, ProductVariation, \
DiscountCode
from paypal.standard.ipn.signals import payment_was_successful

def payment_complete(sender, **kwargs):
    """Performs the same logic as the code in
    cartridge.shop.models.Order.complete(), but fetches the session,
    order, and cart objects from storage, rather than relying on the
    request object being passed in (which it isn't, since this is
    triggered on PayPal IPN callback)."""

    ipn_obj = sender

    if ipn_obj.custom and ipn_obj.payment_status == "Completed":
        s_key, cart_pk = ipn_obj.custom.split(',')
        SessionStore = import_module(settings.SESSION_ENGINE) \
                           .SessionStore
        session = SessionStore(s_key)

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

payment_was_successful.connect(payment_complete)


class HomePage(Page, RichText):
    '''
    A page representing the format of the home page
    '''

    content_heading = models.CharField(max_length=200,
        default="About us!")
    featured_portfolio = models.ForeignKey("Portfolio", blank=True, null=True,
        help_text="If selected items from this portfolio will be featured "
                  "on the home page.")
    

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Slide(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="slides")
    image = FileField(verbose_name=_("Image"),
        upload_to=upload_to("taobay.Slide.image", "slider"),
        format="Image", max_length=255, null=True, blank=True)



COLUMN_CHOICES = (
	('6', 'Two columns'), # 2 columns use span6
	('4', 'Three columns'), # 3 columns use span4
	('3', 'Four columns'), # 4 columns use span3
)

class Portfolio(Page):
    '''
    A collection of individual portfolio items
    '''	
    content = RichTextField(blank = True)
    columns = models.CharField(max_length=1,choices=COLUMN_CHOICES,default='3')
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

class PortfolioItem(Page, RichText):
    
    
    featured_image = FileField(verbose_name=_("Featured Image"), upload_to=
			upload_to("flaunt.PortfolioItem.featured_image", "portfolio"),\
			format="Image", max_length=255, null=True, blank=True)

    short_description = RichTextField(blank=True)
    categories = models.ManyToManyField("PortfolioItemCategory", 
			verbose_name=_("Categories"),\
			blank=True, related_name="portfolioitems")
    href = models.CharField(max_length=2000, blank=True,\
			help_text = "A link to the finished project (optional)")
    class Meta:
	verbose_name = _("Portfolio item")
	verbose_name_plural = _("Portfolio items")


class PortfolioItemImage(Orderable):
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",\
	    upload_to=upload_to("flaunt.PortfolioItemImage.file", "portfolio items"))
    class Meta:
	verbose_name="Portfolio Item Image"
	verbose_name_plural="Portfolio Item Images"

class PortfolioItemCategory(Slugged):
    """
	A category for grouping portfolio items into a series.
    """
    
    class Meta:
	verbose_name=_("Portfolio Item Category")
	verbose_name_plural=_("Portfolio Item Categories")
	ordering=("title",)

#class that has one-to-one relationship with Cartridge's Product and add fields to it
class AddFieldsToProducts(Orderable):
	product = models.ForeignKey(Product, related_name="supplementary")
	short_desco = RichTextField(blank=True)


class Countrylist(models.Model):
	country = models.CharField(max_length=100)
	def __unicode__(self):
		return self.country

class CarrierlistPriority(models.Model):
	carrier = models.CharField(max_length=100)
	countries = models.ManyToManyField(Countrylist)
	def __unicode__(self):
		return self.carrier

class CarrierlistRegular(models.Model):
    carrier = models.CharField(max_length=100)
    countries = models.ManyToManyField(Countrylist)
    def __unicode__(self):
        return self.carrier
