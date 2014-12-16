from mezzanine import template
register = template.Library()
@register.filter(name='get_charge')
def get_ppl_charge(f):
	return f.as_p().split()[14].split("\"")[1]
