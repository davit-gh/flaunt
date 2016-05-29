from cartridge.shop.models import Category

def get_men_women_categories(request):
	amd_categories = Category.objects.filter(title__startswith="AMD")
	intel_categories = Category.objects.filter(title__startswith="Intel")
	#product_categories = Category.objects.get(title="Products").children.published()
	#product_titles = map(lambda x: x.title, product_categories)
	amd_titles = map(lambda x: x.title, amd_categories)
	amd_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in amd_categories]

	intel_titles = map(lambda x: x.title, intel_categories)
	intel_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in intel_categories]
	#product_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in product_categories]
	context = {
		'amd': dict(zip(amd_titles,amd_subtitles)),
		'intel': dict(zip(intel_titles,intel_subtitles)),
		#'women': dict(zip(product_titles,product_subtitles)),
	}
	return context