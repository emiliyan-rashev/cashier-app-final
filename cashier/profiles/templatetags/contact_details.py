from django import template
from django.contrib.auth import get_user_model

from cashier.profiles.models import UserProfile

register = template.Library()
UserModel = get_user_model()

@register.inclusion_tag('base/contact_details.html', takes_context=True)
def contact_details(context):
    superuser_email = 'default@email.com'
    superuser_phone = '0123456789'
    superuser_first_name = 'Default_First_Name'
    superuser_last_name = 'Default_Last_Name'

    if UserModel.objects.filter(is_superuser=True):
        if UserProfile.objects.get(pk=UserModel.objects.filter(is_superuser=True).first().id).first_name != '':
            first_superuser_profile = UserProfile.objects.get(pk=UserModel.objects.filter(is_superuser=True).first().id)
            superuser_email = first_superuser_profile.email
            superuser_phone = first_superuser_profile.phone_number
            superuser_first_name = first_superuser_profile.first_name
            superuser_last_name = first_superuser_profile.last_name

    return {
        'phone_number' : superuser_phone,
        'e_mail' : superuser_email,
        'first_name' : superuser_first_name,
        'last_name' : superuser_last_name,
    }