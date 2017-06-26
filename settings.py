from __future__ import absolute_import, unicode_literals

######################
# CARTRIDGE SETTINGS #
######################
RATINGS_RANGE = range(5,1,-1)
# The following settings are already defined in cartridge.shop.defaults
# with default values, but are common enough to be put here, commented
# out, for convenient overriding.

# Sequence of available credit card types for payment.
# SHOP_CARD_TYPES = ("Mastercard", "Visa", "Diners", "Amex")

# Setting to turn on featured images for shop categories. Defaults to False.
SHOP_CATEGORY_USE_FEATURED_IMAGE = True
SHOP_USE_UPSELL_PRODUCTS = True
SHOP_USE_RELATED_PRODUCTS = True
SHOP_USE_RATINGS = False
ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "first_name",
    "last_name",
)
ACCOUNTS_NO_USERNAME = False
ACCOUNTS_VERIFICATION_REQUIRED = False
SHOP_CHECKOUT_ACCOUNT_REQUIRED = False
PRIMARY_PAYMENT_PROCESSOR_IN_USE = False
SECONDARY_PAYMENT_PROCESSORS = (
    ('paypal', {
        'name' : 'Pay With Pay-Pal',
        'form' : 'payments.multipayments.forms.paypal.PaypalSubmissionForm'
    }),
)
PAYPAL_CURRENCY = "USD"
PAYPAL_BUSINESS = "cartforbrand@gmail.com"
PAYPAL_RECEIVER_EMAIL = PAYPAL_BUSINESS
# Use this to enable https on return URLs.  This is strongly recommended! (Except for sandbox)
PAYPAL_RETURN_WITH_HTTPS = False
# URL is sent to PayPal as the for returning to a 'complete' landing page.
PAYPAL_RETURN_URL = lambda cart, uuid, order_form: ('shop_complete', None, None)
# URL is sent to PayPal as the URL to callback to for PayPal IPN.
# Set to None if you do not wish to use IPN.
PAYPAL_IPN_URL = lambda cart, uuid, order_form: ('paypal.standard.ipn.views.ipn', None, {})
# URL the secondary-payment-form is submitted to
# For real use set to 'https://www.paypal.com/cgi-bin/webscr'
PAYPAL_SUBMIT_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
# Set an alternative OrderForm class for the checkout process.
SHOP_CHECKOUT_FORM_CLASS = 'cartridge.shop.forms.OrderForm'
# For real use set to False
PAYPAL_TEST = False
# If True, the checkout process is split into separate
# billing/shipping and payment steps.
SHOP_CHECKOUT_STEPS_SPLIT = True

# If True, the checkout process has a final confirmation step before
# completion.
SHOP_CHECKOUT_STEPS_CONFIRMATION = True
SHOP_PAYMENT_STEP_ENABLED = False
# Controls the formatting of monetary values accord to the locale
# module in the python standard library. If an empty string is
# used, will fall back to the system's locale.
# SHOP_CURRENCY_LOCALE = ""

# Dotted package path and class name of the function that
# is called on submit of the billing/shipping checkout step. This
# is where shipping calculation can be performed and set using the
# function ``cartridge.shop.utils.set_shipping``.
SHOP_HANDLER_BILLING_SHIPPING = \
                           "flaunt.shop.checkout.billship_handler"

# Dotted package path and class name of the function that
# is called once an order is successful and all of the order
# object's data has been created. This is where any custom order
# processing should be implemented.
# SHOP_HANDLER_ORDER = "cartridge.shop.checkout.default_order_handler"

# Dotted package path and class name of the function that
# is called on submit of the payment checkout step. This is where
# integration with a payment gateway should be implemented.
# SHOP_HANDLER_PAYMENT = "cartridge.shop.checkout.default_payment_handler"

# Sequence of value/name pairs for order statuses.
# SHOP_ORDER_STATUS_CHOICES = (
#     (1, "Unprocessed"),
#     (2, "Processed"),
# )

# Sequence of value/name pairs for types of product options,
# eg Size, Colour.
SHOP_OPTION_TYPE_CHOICES = (
     (1, "Size"),
     (2, "Colour"),
     (3, "Material")
 )

# Sequence of indexes from the SHOP_OPTION_TYPE_CHOICES setting that
# control how the options should be ordered in the admin,
# eg for "Colour" then "Size" given the above:
# SHOP_OPTION_ADMIN_ORDER = (2, 1)

######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for convenient
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
# ADMIN_MENU_ORDER = (
#     ("Content", ("pages.Page", "blog.BlogPost",
#        "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
#     ("Shop", ("shop.Product", "shop.ProductOption", "shop.DiscountCode",
#         "shop.Sale", "shop.Order")),
#     ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
#     ("Users", ("auth.User", "auth.Group",)),
# )

# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
# DASHBOARD_TAGS = (
#     ("blog_tags.quick_blog", "mezzanine_tags.app_list"),
#     ("comment_tags.recent_comments",),
#     ("mezzanine_tags.recent_actions",),
# )

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

# PAGE_MENU_TEMPLATES = (
#     (1, "Top navigation bar", "pages/menus/dropdown.html"),
#     (2, "Left-hand tree", "pages/menus/tree.html"),
#     (3, "Footer", "pages/menus/footer.html"),
# )



# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
EXTRA_MODEL_FIELDS = (
      (
    	  "cartridge.shop.models.Product.short_desc",
    	  "TextField",
    	  ("Short desc",),
    	  {"blank": True},
      ),
      (
          "cartridge.shop.models.Product.additional",
          "mezzanine.core.fields.RichTextField",
          ("Additional Info",),
          {"blank": True},
      ),
      (
        "cartridge.shop.models.Order.callback_uuid",
        "django.db.models.CharField",
        (),
        {"blank" : False, "max_length" : 36, "default": ""},
      ),
      (
        "cartridge.shop.models.Order.tracking_numbe",
        "django.db.models.CharField",
        (),
        {"blank" : True, "max_length" : 36, "default": "Not updated yet."},
      ),
      (
        "cartridge.shop.models.Order.carrie",
        "django.db.models.CharField",
        (),
        {"blank" : True, "max_length" : 36, "default": "Not updated yet."},
      ),
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         ("Image",),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         ("Another name",),
#         {"blank": True, "default": 1},
#     ),
)

# Setting to turn on featured images for blog posts. Defaults to False.
#
BLOG_USE_FEATURED_IMAGE = True

# If True, the south application will be automatically added to the
# INSTALLED_APPS setting.
USE_SOUTH = True


########################
# MAIN DJANGO SETTINGS #
########################

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    ('Davit', '2244022248@qq.com'),
)
MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['128.199.160.27', 'you-name-it.net', 'www.you-name-it.net']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Asia/Yerevan"

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# Supported languages
_ = lambda s: s
LANGUAGES = (
    ('en', _('English')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 2
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1",)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend",)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}


#########
# PATHS #
#########

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "flaunt",
    "partygames",
    "postmark",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "robots",
    "cartridge.shop",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
#    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.accounts",
    "payments.multipayments",
    "paypal.standard.ipn",
    #"mezzanine.mobile",
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    "payments.multipayments.context_processors.settings",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.static",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
    "flaunt.context_processors.get_men_women_categories",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cartridge.shop.middleware.ShopMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
    
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

###################
# DEPLOY SETTINGS #
###################

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "SSH_USER": "", # SSH username
#     "SSH_PASS":  "", # SSH password (consider key-based authentication)
#     "SSH_KEY_PATH":  "", # Local path to SSH key file, for key-based auth
#     "HOSTS": [], # List of hosts to deploy to
#     "VIRTUALENV_HOME":  "", # Absolute remote path for virtualenvs
#     "PROJECT_NAME": "", # Unique identifier for project
#     "REQUIREMENTS_PATH": "", # Path to pip requirements, relative to project
#     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
#     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
#     "LIVE_HOSTNAME": "www.example.com", # Host for public site.
#     "REPO_URL": "", # Git or Mercurial remote repo URL for the project
#     "DB_PASS": "", # Live database password
#     "ADMIN_PASS": "", # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass

####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

########################
# SOCIAL ICON SETTINGS #
########################

SITE_TITLE = "Cart4brand"


EMAIL_BACKEND = "postmark.backends.PostmarkBackend"
POSTMARK_API_KEY = "42eb9eb5-4012-4f34-b747-ecd64cfef567"
POSTMARK_API_USER = "bigelow"
POSTMARK_API_PASSWORD = "verysecure"
DEFAULT_FROM_EMAIL = 'info@cart4brand.com'
SHOP_ORDER_FROM_EMAIL  = DEFAULT_FROM_EMAIL


MY_BTC_ADDRESS = '1DcRmYAEGc8CEXiPQr6wqGxWp6H44mH7wX'
BTC_SECRET = 'so3vi54cibusqx71yerjiqvpk2n5wov3cd29paz4'

SOUTH_MIGRATION_MODULES = {
        'robots': 'robots.south_migrations',
}

HOST_THEMES = [('www.cart4brand.com', 'flaunt'),
               ('cart4brand.com', 'flaunt'),
               ('games4parties.com', 'partygames'),
               ('localhost', 'flaunt'),
               ('127.0.0.1', 'partygames')]

