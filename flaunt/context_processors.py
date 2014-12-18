from cartridge.shop.models import Category

def get_men_women_categories(request):
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