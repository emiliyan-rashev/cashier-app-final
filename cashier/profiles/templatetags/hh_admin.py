from django import template

from cashier.profiles.models import UserProfile

register = template.Library()


@register.inclusion_tag("households/hh_admin_link.html", takes_context=True)
def hh_admin(context):
    user_profile = UserProfile.objects.get(pk=context.request.user.id)
    return {
        "is_hh_admin": user_profile.is_household_admin,
        "apartment": user_profile.apartment,
    }
