from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from cashier.profiles.forms import EditProfileForm
from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser
from cashier.users.views import logout_view

def ViewProfileView(request,pk):
    profile = UserProfile.objects.get(pk=pk)
    context = {
        'profile' : profile,
    }
    return render(request, 'view_profile.html', context)

class EditProfileView(UpdateView):
    model = UserProfile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm
    def get_object(self, queryset=None):
        return self.model.objects.get(user=self.request.user)
    success_url = reverse_lazy('home_view')

def confirm_delete(request,pk):
    if request.method == 'POST':
        return DeleteProfileView(request,pk)
    context = {
        'profile_owner' : cashierUser.objects.get(pk=pk),
    }
    return render(request, 'delete_profile.html', context)

def DeleteProfileView(request,pk):
    user = cashierUser.objects.get(pk=pk)
    user.is_active = False
    profile = UserProfile.objects.get(pk=pk)
    profile.live_in_apartment = False
    user.save()
    profile.save()
    if user == request.user:
        return logout_view(request)
    else:
        return redirect('home_view')
