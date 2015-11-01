from .models import HomePage, Slide, FAQPage, FAQ
from cartridge.shop.models import Product# Category
from mezzanine.conf import settings
from django.template.defaultfilters import slugify
from mezzanine.utils.views import paginate

#for ajax form processor
from mezzanine.pages.page_processors import processor_for
from mezzanine.pages.models import Page
from flaunt.views import product
from collections import OrderedDict
import pdb 


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
	product_vars = [product(request, prod) for prod in products]
	#pdb.set_trace()
	return {'products':OrderedDict(zip(products,product_vars)), 'slider_images': slider_images}

@processor_for(FAQPage)
def home_processor(request, page):
	qas = FAQ.objects.all()
	return {'qas': qas}
