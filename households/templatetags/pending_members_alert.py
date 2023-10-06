from django import template
from django.db.models import Q

from households.models import HouseholdProfile
from households.views import inactive_users
from profiles.models import UserProfile

register = template.Library()


@register.inclusion_tag("households/hh_pending_members_alert.html", takes_context=True)
def pending_members_alert(context):
    if context.request.user.is_authenticated:
        user_profile = UserProfile.objects.get(pk=context.request.user.id)
        if context.request.user.is_superuser:
            apartments_with_admins = UserProfile.objects.filter(
                Q(is_household_admin=True),
                ~Q(apartment=user_profile.apartment),
                ~Q(user__in=inactive_users()),
            ).values_list("apartment", flat=True)
            member_list = UserProfile.objects.filter(
                Q(household=None),
                ~Q(apartment__in=apartments_with_admins),
                ~Q(apartment=None),
                ~Q(user__in=inactive_users()),
            )
            if (len(set(member_list.values_list("apartment", flat=True))) == 1) and (
                HouseholdProfile.objects.filter(
                    apartment=member_list.values_list("apartment", flat=True).first()
                ).exists()
            ):
                household = member_list.values_list("apartment", flat=True).first()
            else:
                household = None
            profile_type = "superuser"
        elif user_profile.is_household_admin:
            household = user_profile.apartment
            member_list = UserProfile.objects.filter(
                Q(household=None), Q(apartment=household), ~Q(user__in=inactive_users())
            )
            profile_type = "hh_admin"
        else:
            member_list = None
            profile_type = "user"
            household = None
    else:
        member_list = None
        profile_type = "user"
        household = None
    return {
        "member_list": member_list,
        "profile_type": profile_type,
        "household": household,
    }
