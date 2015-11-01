from mezzanine import template
from mezzanine.forms.forms import FormForForm
from mezzanine.core.models import Displayable
import pdb

register = template.Library()

@register.as_tag
def form_from_page(slug):
    #pdb.set_trace()
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        return None

    return FormForForm(page.form, None, None)
