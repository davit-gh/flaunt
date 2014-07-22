from .models import HomePage, Portfolio, PortfolioItem, PortfolioItemCategory, Slide
from mezzanine.pages.page_processors import processor_for
from cartridge.shop.models import Cart, Product
from forms import CountryForm

#for ajax form processor
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson

from django.template import RequestContext

from mezzanine.conf import settings
from mezzanine.forms.forms import FormForForm
from mezzanine.forms.models import Form
from mezzanine.forms.page_processors import format_value
from mezzanine.forms.signals import form_invalid, form_valid
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.email import send_mail_template
from mezzanine.utils.views import is_spam

from cartridge.shop.models import Category
@processor_for(Portfolio)
def portfolio_processor(request, page):
	SCREEN_WIDTH = 1170
	IMAGE_RATIO = 370.0 / 185.0
	# Adds a portfolio's portfolio items to the context
	items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
	
	categories = PortfolioItemCategory.objects.filter(portfolioitems__in=items).distinct()
	#Adjust grid size based on the values of 'columns'
	
	
	return {"items":items, "categories": categories}

@processor_for(PortfolioItem)
def portfolioitem_processor(request, page):
	portfolioitem = PortfolioItem.objects.published(for_user=request.user).prefetch_related(\
		'categories', 'images').get(id=page.portfolioitem.id)
	return {'portfolioitem':portfolioitem}

@processor_for(HomePage)
def home_processor(request, page):
	items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
	items = items.filter(parent=page.homepage.featured_portfolio)
	return {'items':items}

@processor_for(Category)
def shop_processor(request, page):
	slider_images = Slide.objects.all()
	return {'slider_images': slider_images}



