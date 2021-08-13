from django import template

from cashier.profiles.models import UserProfile

register = template.Library()

@register.inclusion_tag('profiles/profile_incomplete_alert.html', takes_context=True)
def profile_is_complete(context):
    user_profile = UserProfile.objects.get(pk=context.request.user.id)
    if (user_profile.first_name != '') and (user_profile.last_name != '') and (not user_profile.email.isdigit()) and \
    (user_profile.phone_number.isdigit()) and (user_profile.apartment > 0):
        profile_complete = True
    else:
        profile_complete = False
    return {
            'profile_complete' : profile_complete,
            'profile_user' : UserProfile.objects.get(pk=context.request.user.id).user,
        }
