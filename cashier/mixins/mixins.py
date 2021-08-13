from urllib.parse import urlparse

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, resolve_url

#test link - http://127.0.0.1:8080/household/profile/302/edit
from django.urls import reverse_lazy

from cashier.profiles.models import UserProfile

class NotLoggedInRequired(AccessMixin):
    def handle_no_permission(self):
        return render(request=self.request, template_name='base/home_view.html')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class SuperUserRequiredMixin(AccessMixin):
    permission_denied_message = 'You need to be a super user to view this page!'
    context = {
        'error_message' : permission_denied_message,
    }
    def handle_no_permission(self):
        return render(request=self.request, template_name='base/home_view.html', context=self.context)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class HouseholdAdminRequiredMixin(AccessMixin):
    permission_denied_message = 'You need to be a household admin to view this page!'
    context = {
        'error_message' : permission_denied_message,
    }
    def handle_no_permission(self):
        return render(request=self.request, template_name='base/home_view.html', context=self.context)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = self.request.build_absolute_uri()
            resolved_login_url = resolve_url(self.get_login_url())
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (
                (not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)
            ):
                path = self.request.get_full_path()
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
        is_hh_admin = request.resolver_match.kwargs['pk'] == UserProfile.objects.get(pk=request.user.id).apartment
        if not (is_hh_admin or request.user.is_superuser):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class HouseholdAdminOfUserRequiredMixin(AccessMixin):
    permission_denied_message = 'You need to be a household admin to view this page!'
    context = {
        'error_message' : permission_denied_message,
    }
    def handle_no_permission(self):
        return render(request=self.request, template_name='base/home_view.html', context=self.context)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = self.request.build_absolute_uri()
            resolved_login_url = resolve_url(self.get_login_url())
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (
                (not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)
            ):
                path = self.request.get_full_path()
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
        is_hh_admin = (UserProfile.objects.get(pk=request.resolver_match.kwargs['pk']).apartment == UserProfile.objects.get(pk=request.user.id).apartment) and (UserProfile.objects.get(pk=request.user.id).is_household_admin)
        if not (is_hh_admin or request.user.is_superuser):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OwnerOrSuperUserRequiredMixin(AccessMixin):
    permission_denied_message = "You need to be owner or superuser to access this page!"
    context = {
        'error_message' : permission_denied_message,
    }
    def handle_no_permission(self):
        return render(request=self.request, template_name='base/home_view.html', context=self.context)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = self.request.build_absolute_uri()
            resolved_login_url = resolve_url(self.get_login_url())
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (
                (not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)
            ):
                path = self.request.get_full_path()
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
        is_owner = request.resolver_match.kwargs['pk'] == request.user.id
        if not (is_owner or request.user.is_superuser):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class OwnerOrHouseholdAdminOrSuperUserRequiredMixin(AccessMixin):
    permission_denied_message = "You need to be owner or household admin of this user's household or superuser to access this page!"
    context = {
        'error_message' : permission_denied_message,
    }
    def handle_no_permission(self):
        return render(request=self.request, template_name='base/home_view.html', context=self.context)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = self.request.build_absolute_uri()
            resolved_login_url = resolve_url(self.get_login_url())
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (
                (not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)
            ):
                path = self.request.get_full_path()
            return redirect_to_login(
                path,
                resolved_login_url,
                self.get_redirect_field_name(),
            )
        is_owner = request.resolver_match.kwargs['pk'] == request.user.id
        is_hh_admin = UserProfile.objects.get(pk=request.resolver_match.kwargs['pk']).apartment == UserProfile.objects.get(pk=request.user.id).apartment
        if not (is_owner or is_hh_admin or request.user.is_superuser):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)