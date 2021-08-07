from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from cashier.households.models import HouseholdProfile
from cashier.profiles.models import UserProfile

def HouseholdProfileView(request,pk):
    household = HouseholdProfile.objects.get(pk=pk)
    curr_user = UserProfile.objects.get(pk=request.user.id)
    hh_members = household.userprofile_set.all().filter(live_in_apartment=True)
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

def HouseholdAdminView(request):
    households = HouseholdProfile.objects.all()
    context = {
        'households': households,
    }
    return render(request, 'admin_households.html', context)