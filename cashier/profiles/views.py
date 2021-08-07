from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from cashier.profiles.forms import EditProfileForm
from cashier.profiles.models import UserProfile
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

def confirm_delete(request):
    if request.method == 'POST':
        return DeleteProfileView(request)
    return render(request, 'delete_profile.html')

def DeleteProfileView(request):
    user = request.user
    user.is_active = False
    profile = UserProfile.objects.get(pk=user.pk)
    profile.live_in_apartment = False
    user.save()
    profile.save()
    return logout_view(request)
