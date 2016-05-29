from django.contrib.sitemaps import Sitemap
from cartridge.shop.models import Product

class FlauntSitemap(Sitemap):
	changefreq = "weekly"
	priority = 0.5

	def items(self):
		return Product.objects.all()