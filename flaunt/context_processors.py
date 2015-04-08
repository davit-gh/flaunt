from cartridge.shop.models import Category

def get_men_women_categories(request):
	#men_categories = Category.objects.get(title="Men").children.published()
	product_categories = Category.objects.get(title="Women").children.published()
	product_titles = map(lambda x: x.title, product_categories)
	#men_titles = map(lambda x: x.title, men_categories)
	#men_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in men_categories]
	product_subtitles = [[(subcat.title, subcat.slug) for subcat in cat.children.published()] for cat in product_categories]
	context = {
		#'men': dict(zip(men_titles,men_subtitles)),
		'women': dict(zip(product_titles,product_subtitles)),
	}
	return context