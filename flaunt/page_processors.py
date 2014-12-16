from .models import HomePage, Portfolio, PortfolioItem, PortfolioItemCategory, Slide
from mezzanine.pages.page_processors import processor_for
from cartridge.shop.models import Cart, Product, Category
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
from mezzanine.pages.models import Page
from mezzanine.utils.email import send_mail_template
from mezzanine.utils.views import is_spam
from django.template.defaultfilters import slugify
from mezzanine.utils.views import paginate
from cartridge.shop.models import Category
import pdb 

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


def get_men_women_categories():
	men_categories = Category.objects.get(title="Men").children.published()
	women_categories = Category.objects.get(title="Women").children.published()
	women_titles = map(lambda x: x.title, women_categories)
	men_titles = map(lambda x: x.title, men_categories)
	men_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in men_categories]
	women_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in women_categories]
	context = {
		'men': dict(zip(men_titles,men_subtitles)),
		'women': dict(zip(women_titles,women_subtitles)),
	}
	return context

@processor_for(Category)
def category_processor(request, page):
	return {'context': get_men_women_categories()}

@processor_for(HomePage)
def home_processor(request, page):
	#items = PortfolioItem.objects.published(for_user=request.user).prefetch_related('categories')
	#items = items.filter(parent=page.homepage.featured_portfolio)
	#pdb.set_trace()
	products = Product.objects.published(for_user=request.user)#.filter(page.category.filters()).distinct()
    
	sort_options = [(slugify(option[0]), option[1])
		            for option in settings.SHOP_PRODUCT_SORT_OPTIONS]
	sort_by = request.GET.get("sort", sort_options[0][1])
	products = paginate(products.order_by(sort_by),
		                request.GET.get("page", 1),
		                settings.SHOP_PER_PAGE_CATEGORY,
		                settings.MAX_PAGING_LINKS)
	products.sort_by = sort_by

	slider_images = Slide.objects.all()
	
	#pdb.set_trace()
	return {'products':products, 'slider_images': slider_images, 'context': get_men_women_categories()}




