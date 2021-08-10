from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView, ListView
from django.views.generic.base import View

from cashier.households.forms import UserApproveForm
from cashier.households.models import HouseholdProfile
from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser

#not a view - shouldn't be here
def inactive_users():
    return cashierUser.objects.filter(is_active=False)

def household_profile_view(request,pk):
    household = HouseholdProfile.objects.get(pk=pk)
    curr_user = UserProfile.objects.get(pk=request.user.id)
    members_in_hh = UserProfile.objects.filter(Q(live_in_apartment=True), Q(household=household), ~Q(user__in=inactive_users()))
    admins_in_hh = UserProfile.objects.filter(Q(is_household_admin=True), Q(household=household), ~Q(user__in=inactive_users()))
    not_approved_members = UserProfile.objects.filter(Q(apartment=household.apartment), Q(household=None), ~Q(user__in=inactive_users()))
    not_living_in_hh = UserProfile.objects.filter(Q(live_in_apartment=False), Q(household=household), ~Q(user__in=inactive_users()))
    is_hh_admin = curr_user.is_household_admin and household.apartment == curr_user.apartment
    context = {
        'members_in_hh' : members_in_hh,
        'admins_in_hh' : admins_in_hh,
        'not_approved_members' : not_approved_members,
        'not_living_in_hh' : not_living_in_hh,
        'household' : household,
        'is_hh_admin': is_hh_admin,
	}
    return render(request, 'hh_profile_view.html', context)

class HouseholdEditProfileView(UpdateView):
    model = HouseholdProfile
    fields = ('apartment_percent_ideal_parts',)
    template_name = 'hh_profile_edit.html'
    def get_success_url(self):
        return reverse_lazy('hh_profile', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

class HouseholdRemoveUser(UpdateView):
    model = UserProfile
    fields = ('live_in_apartment',)
    template_name = 'hh_remove_user.html'
    def get_success_url(self):
        return reverse_lazy('hh_profile', kwargs={'pk': self.object.apartment})

class HouseholdApproveUser(FormView):
    form_class = UserApproveForm

    def get_success_url(self):
        pk_from_url = self.request.resolver_match.kwargs['pk']
        self.object = UserProfile.objects.get(pk=pk_from_url)
        return reverse_lazy('hh_profile', kwargs={'pk': self.object.apartment})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            pk_from_url = self.request.resolver_match.kwargs['pk']
            profile = UserProfile.objects.get(pk=pk_from_url)
            success_url = self.get_success_url()
            if form.cleaned_data['approval'] == 'Approve':
                hh_profile = HouseholdProfile(pk=profile.apartment, apartment=profile.apartment)
                hh_profile.save()
                profile.household = hh_profile
                profile.save()
            elif form.cleaned_data['approval'] == 'Reject':
                profile.live_in_apartment = False
                profile.apartment = 0
                profile.save()
            return HttpResponseRedirect(success_url)
        else:
            return self.form_invalid(form)
    template_name = 'hh_remove_user.html'

def all_pending_members(request):
    not_approved_members = UserProfile.objects.filter(Q(household=None),~Q(apartment=0), ~Q(user__in=inactive_users()))
    existing_apartments = HouseholdProfile.objects.all().values_list('apartment', flat=True)
    context = {
        'not_approved_members': not_approved_members,
        'existing_apartments' : existing_apartments,
    }
    return render(request, 'hh_all_pending_members.html', context)

def urgent_pending_members(request):
    apartments_with_admins = UserProfile.objects.filter(Q(is_household_admin=True), ~Q(apartment=UserProfile.objects.get(pk=request.user.id).apartment), ~Q(user__in=inactive_users())).values_list('apartment', flat=True)
    not_approved_members = UserProfile.objects.filter(Q(household=None),~Q(apartment=0), ~Q(apartment__in=apartments_with_admins), ~Q(user__in=inactive_users()))
    existing_apartments = HouseholdProfile.objects.all().values_list('apartment', flat=True)
    context = {
        'not_approved_members': not_approved_members,
        'existing_apartments' : existing_apartments,
    }
    return render(request, 'hh_urgent_pending_members.html', context)

def household_superuser_view(request):
    households = HouseholdProfile.objects.all()
    context = {
        'households': households,
    }
    return render(request, 'admin_households.html', context)

class SetHouseholdAdmins(UpdateView):
    model = UserProfile
    fields = ('is_household_admin',)
    template_name = 'hh_remove_user.html' #Would be better to rename this file
    def get_success_url(self):
        return reverse_lazy('hh_profile', kwargs={'pk': self.object.apartment})