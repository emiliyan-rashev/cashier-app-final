from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import View, TemplateView
from mixins.form_bootstrap import BootStrapFormMixin
from mixins.mixins import NotLoggedInRequired, SuperUserRequiredMixin
from profiles.forms import EditProfileForm
from users.forms import UserForm
from users.models import ContactDetails

UserModel = get_user_model()


class HomeView(TemplateView):
    template_name = "base/home_view.html"


class ContactView(TemplateView):
    template_name = "base/contact_view.html"

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        if ContactDetails.objects.exists():
            contact_object = ContactDetails.objects.first()
            self.extra_context = {
                "email": contact_object.email,
                "phone": contact_object.phone,
                "first_name": contact_object.first_name,
                "last_name": contact_object.last_name,
            }
            kwargs.update(self.extra_context)
        return kwargs


class EditContactView(BootStrapFormMixin, SuperUserRequiredMixin, UpdateView):
    model = ContactDetails
    fields = "__all__"
    template_name = "profiles/edit_profile.html"
    success_url = reverse_lazy("contact_view")

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=1)


class RegisterView(BootStrapFormMixin, NotLoggedInRequired, View):
    def get(self, request):
        user_form = UserForm()
        profile_form = EditProfileForm()
        data = {
            "user_form": user_form,
            "profile_form": profile_form,
        }
        self.apply_bootstrap_classes(user_form)
        self.apply_bootstrap_classes(profile_form)

        return render(request, "users/register_view.html", data)

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = EditProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.id = request.user.id
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect("home_view")
        else:
            self.apply_bootstrap_classes(user_form)
            self.apply_bootstrap_classes(profile_form)
            context = {
                "user_form": user_form,
                "profile_form": profile_form,
            }
            return render(request, "users/register_view.html", context)


class UserLoginView(BootStrapFormMixin, LoginView):
    template_name = "users/login_view.html"
    redirect_authenticated_user = True
