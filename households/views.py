from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView
from django.views.generic.base import TemplateView
from households.forms import UserApproveForm
from households.models import HouseholdProfile
from mixins.form_bootstrap import BootStrapFormMixin
from mixins.mixins import (
    SuperUserRequiredMixin,
    HouseholdAdminRequiredMixin,
    HouseholdAdminOfUserRequiredMixin,
)
from profiles.models import UserProfile
from users.models import CashierUser


# not a view - shouldn't be here
def inactive_users():
    return CashierUser.objects.filter(is_active=False)


class HouseholdProfileView(LoginRequiredMixin, TemplateView):
    template_name = "households/hh_profile_view.html"

    def get_context_data(self, **kwargs):
        pk_from_url = self.request.resolver_match.kwargs["pk"]
        household = HouseholdProfile.objects.get(pk=pk_from_url)
        curr_user = UserProfile.objects.get(pk=self.request.user.id)
        members_in_hh = UserProfile.objects.filter(
            Q(live_in_apartment=True),
            Q(household=household),
            ~Q(user__in=inactive_users()),
        )
        admins_in_hh = UserProfile.objects.filter(
            Q(is_household_admin=True),
            Q(household=household),
            ~Q(user__in=inactive_users()),
        )
        not_approved_members = UserProfile.objects.filter(
            Q(apartment=household.apartment),
            Q(household=None),
            ~Q(user__in=inactive_users()),
        )
        not_living_in_hh = UserProfile.objects.filter(
            Q(live_in_apartment=False),
            Q(household=household),
            ~Q(user__in=inactive_users()),
        )
        is_hh_admin = (
            curr_user.is_household_admin and household.apartment == curr_user.apartment
        )
        self.extra_context = {
            "members_in_hh": members_in_hh,
            "admins_in_hh": admins_in_hh,
            "not_approved_members": not_approved_members,
            "not_living_in_hh": not_living_in_hh,
            "household": household,
            "is_hh_admin": is_hh_admin,
        }
        kwargs.update(self.extra_context)
        return kwargs


class HouseholdEditProfileView(
    HouseholdAdminRequiredMixin, BootStrapFormMixin, UpdateView
):
    model = HouseholdProfile
    fields = ("apartment_percent_ideal_parts",)
    template_name = "households/hh_profile_edit.html"

    def get_success_url(self):
        return reverse_lazy(
            "hh_profile", kwargs={"pk": self.kwargs.get(self.pk_url_kwarg)}
        )


class HouseholdRemoveUser(
    HouseholdAdminOfUserRequiredMixin, BootStrapFormMixin, UpdateView
):
    model = UserProfile
    fields = ("live_in_apartment",)
    template_name = "households/hh_remove_user.html"

    def get_success_url(self):
        return reverse_lazy("hh_profile", kwargs={"pk": self.object.apartment})


class HouseholdApproveUser(
    HouseholdAdminOfUserRequiredMixin, BootStrapFormMixin, FormView
):
    form_class = UserApproveForm
    template_name = "households/hh_approve_user.html"

    def get_success_url(self):
        pk_from_url = self.request.resolver_match.kwargs["pk"]
        self.object = UserProfile.objects.get(pk=pk_from_url)
        if self.object.household != None:
            return reverse_lazy("hh_profile", kwargs={"pk": self.object.apartment})
        else:
            return reverse_lazy("view_profile", kwargs={"pk": self.object.user.id})

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        pk_from_url = self.request.resolver_match.kwargs["pk"]
        self.object = UserProfile.objects.get(pk=pk_from_url)
        self.extra_context = {
            "curr_user": self.object.user,
            "curr_apt": self.object.apartment,
            "form": self.get_form(),
        }
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            pk_from_url = self.request.resolver_match.kwargs["pk"]
            profile = UserProfile.objects.get(pk=pk_from_url)
            success_url = self.get_success_url()
            if form.cleaned_data["approval"] == "Approve":
                hh_profile = HouseholdProfile(
                    pk=profile.apartment, apartment=profile.apartment
                )
                hh_profile.save()
                profile.household = hh_profile
                profile.save()
            elif form.cleaned_data["approval"] == "Reject":
                profile.live_in_apartment = False
                profile.apartment = None
                profile.save()
            return HttpResponseRedirect(success_url)
        else:
            return self.form_invalid(form)


class AllPendingMembersView(SuperUserRequiredMixin, TemplateView):
    template_name = "households/hh_all_pending_members.html"

    def get_context_data(self, **kwargs):
        not_approved_members = UserProfile.objects.filter(
            Q(household=None), ~Q(apartment=None), ~Q(user__in=inactive_users())
        )
        existing_apartments = HouseholdProfile.objects.all().values_list(
            "apartment", flat=True
        )
        self.extra_context = {
            "not_approved_members": not_approved_members,
            "existing_apartments": existing_apartments,
        }
        kwargs.update(self.extra_context)
        return kwargs


class UrgentPendingMembersView(SuperUserRequiredMixin, TemplateView):
    template_name = "households/hh_urgent_pending_members.html"

    def get_context_data(self, **kwargs):
        apartments_with_admins = UserProfile.objects.filter(
            Q(is_household_admin=True),
            ~Q(apartment=UserProfile.objects.get(pk=self.request.user.id).apartment),
            ~Q(user__in=inactive_users()),
        ).values_list("apartment", flat=True)
        not_approved_members = UserProfile.objects.filter(
            Q(household=None),
            ~Q(apartment=None),
            ~Q(apartment__in=apartments_with_admins),
            ~Q(user__in=inactive_users()),
        )
        existing_apartments = HouseholdProfile.objects.all().values_list(
            "apartment", flat=True
        )
        self.extra_context = {
            "not_approved_members": not_approved_members,
            "existing_apartments": existing_apartments,
        }
        kwargs.update(self.extra_context)
        return kwargs


class HouseholdSuperuserView(SuperUserRequiredMixin, TemplateView):
    template_name = "households/admin_households.html"

    def get_context_data(self, **kwargs):
        households = HouseholdProfile.objects.all()
        self.extra_context = {
            "households": households,
        }
        kwargs.update(self.extra_context)
        return kwargs


class SetHouseholdAdmins(
    HouseholdAdminOfUserRequiredMixin, BootStrapFormMixin, UpdateView
):
    model = UserProfile
    fields = ("is_household_admin",)
    template_name = (
        "households/hh_remove_user.html"  # Would be better to rename this file
    )

    def get_success_url(self):
        return reverse_lazy("hh_profile", kwargs={"pk": self.object.apartment})


class HouseHoldMemberPaymentsView(HouseholdAdminRequiredMixin, TemplateView):
    template_name = "payments/hh_member_payments.html"

    def get_context_data(self, **kwargs):
        pk_from_url = self.request.resolver_match.kwargs["pk"]
        household = HouseholdProfile.objects.get(pk=pk_from_url)
        members_in_hh = UserProfile.objects.filter(
            Q(live_in_apartment=True),
            Q(household=household),
            ~Q(user__in=inactive_users()),
        )
        self.extra_context = {
            "members_in_hh": members_in_hh,
        }
        kwargs.update(self.extra_context)
        return kwargs
