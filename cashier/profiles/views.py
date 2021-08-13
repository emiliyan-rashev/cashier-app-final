from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView, FormView, ListView

from cashier.mixins.form_bootstrap import BootStrapFormMixin
from cashier.mixins.mixins import OwnerOrSuperUserRequiredMixin, SuperUserRequiredMixin
from cashier.profiles.forms import EditProfileForm, DeleteProfileForm
from cashier.profiles.models import UserProfile
from cashier.users.models import cashierUser

class ViewProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/view_profile.html'
    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        context = {
            'profile' : profile,
        }
        return self.render_to_response(context)

class EditProfileView(BootStrapFormMixin, OwnerOrSuperUserRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'profiles/edit_profile.html'
    form_class = EditProfileForm
    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})

class DeleteProfileView(OwnerOrSuperUserRequiredMixin, FormView):
    form_class = DeleteProfileForm
    success_url = reverse_lazy('home_view')
    template_name = 'profiles/delete_profile.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        profile_owner = cashierUser.objects.get(pk=self.request.resolver_match.kwargs['pk'])
        self.extra_context = {'profile_owner' : profile_owner}
        kwargs.update(self.extra_context)
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if form.cleaned_data['result'] == 'Delete':
                user = cashierUser.objects.get(pk=self.request.resolver_match.kwargs['pk'])
                user.is_active = False
                profile = UserProfile.objects.get(pk=self.request.resolver_match.kwargs['pk'])
                profile.live_in_apartment = False
                user.save()
                profile.save()
                if user == request.user:
                    return LogoutView.as_view()
            return HttpResponseRedirect(reverse_lazy('home_view'))
        else:
            return self.form_invalid(form)

class ShowAllUsersView(SuperUserRequiredMixin, ListView):
    model = UserProfile
    ordering = ['apartment']
    paginate_by = 10
    context_object_name = 'all_users'
    template_name = 'users/list_all_users.html'