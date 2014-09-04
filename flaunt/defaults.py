from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import register_setting

#newly registered social links
register_setting(
    name="SOCIAL_LINK_FACEBOOK",
    label=_("Facebook link"),
    description=_("If present a Facebook icon linking here will be in the "
        "header."),
    editable=True,
    default="https://www.facebook.com/YouNameItmarket",
)

register_setting(
    name="SOCIAL_LINK_TWITTER",
    label=_("Twitter link"),
    description=_("If present a Twitter icon linking here will be in the "
        "header."),
    editable=True,
    default="https://twitter.com/_younameit",
)

register_setting(
    name="SOCIAL_LINK_PINTEREST",
    label=_("Pinterest link"),
    description=_("If present a Pinterest icon linking here will be in the "
        "header."),
    editable=True,
    default='http://www.pinterest.com/younameitshop/',
)

#appending new defined setting to TEMPLATE_ACCESSIBLE_SETTINGS
register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=("SOCIAL_LINK_FACEBOOK", "SOCIAL_LINK_TWITTER", "SOCIAL_LINK_PINTEREST"),
    append=True,
)
