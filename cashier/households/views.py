from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, FormView
from cashier.households.forms import UserApproveForm
from cashier.households.models import HouseholdProfile
from cashier.profiles.models import UserProfile

def HouseholdProfileView(request,pk):
    household = HouseholdProfile.objects.get(pk=pk)
    curr_user = UserProfile.objects.get(pk=request.user.id)
    hh_members = UserProfile.objects.filter(Q(apartment=household.apartment), Q(live_in_apartment=True) | Q(household=None))
    is_hh_admin = curr_user.is_household_admin and household.apartment == curr_user.apartment

    context = {
        'hh_members' : hh_members,
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
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data['approve']:
                pk_from_url = self.request.resolver_match.kwargs['pk']
                profile = UserProfile.objects.get(pk=pk_from_url)
                hh_profile = HouseholdProfile(pk=profile.apartment, apartment=profile.apartment)
                hh_profile.save()
                profile.household = hh_profile
                profile.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    template_name = 'hh_remove_user.html'

    def get_success_url(self):
        pk_from_url = self.request.resolver_match.kwargs['pk']
        self.object = UserProfile.objects.get(pk=pk_from_url)
        return reverse_lazy('hh_profile', kwargs={'pk': self.object.apartment})

def HouseholdAdminView(request):
    households = HouseholdProfile.objects.all()
    context = {
        'households': households,
    }
    return render(request, 'admin_households.html', context)