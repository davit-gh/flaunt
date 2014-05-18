from .models import HomePage, Portfolio, PortfolioItem, PortfolioItemCategory, Slide
from mezzanine.pages.page_processors import processor_for

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

@processor_for(Form)
def ajax_form_processor(request, page):
    """
    Handle a Mezzanine form submissions if and only if the request
    is ajax, otherwise the default processor will run.
    """
    print "outside function"
    if request.is_ajax():
	print "inside function"
        form = FormForForm(page.form, RequestContext(request), request.POST or None, request.FILES or None)
        if form.is_valid():
	    print "is valid"
            url = page.get_absolute_url() + "?sent=1"
            if is_spam(request, form, url):
                return redirect(url)
            entry = form.save()
            subject = page.form.email_subject
            if not subject:
                subject = "%s - %s" % (page.form.title, entry.entry_time)
            fields = [(v.label, format_value(form.cleaned_data[k]))
                      for (k, v) in form.fields.items()]
            context = {
                "fields": fields,
                "message": page.form.email_message,
                "request": request,
            }
            email_from = page.form.email_from or settings.DEFAULT_FROM_EMAIL
            email_to = form.email_to()
            if email_to and page.form.send_email:
                send_mail_template(subject, "email/form_response", email_from,
                                   email_to, context, fail_silently=False)
            if not settings.FORMS_DISABLE_SEND_FROM_EMAIL_FIELD:
                # Send from the email entered,
                # unless FORMS_DISABLE_SEND_FROM_EMAIL_FIELD is True.
                email_from = email_to or email_from
            email_copies = page.form.email_copies.split(",")
            email_copies = [e.strip() for e in email_copies if e.strip()]
            if email_copies:
                attachments = []
                for f in form.files.values():
                    f.seek(0)
                    attachments.append((f.name, f.read()))
                send_mail_template(subject, "email/form_response", email_from,
                                   email_copies, context, attachments=attachments,
                                   fail_silently=settings.DEBUG)
            form_valid.send(sender=request, form=form, entry=entry)
            return HttpResponse(simplejson.dumps({'error': False, 'message': page.form.response}),
                    mimetype='application/json')
	print "invalid"
        form_invalid.send(sender=request, form=form)
	return HttpResponse(simplejson.dumps({'error': True, 'message': '<p>Please submit valid data</p>' }),
                mimetype='application/json')
    
