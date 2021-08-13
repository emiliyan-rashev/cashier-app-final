from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView

from cashier.mixins.form_bootstrap import BootStrapFormMixin
from cashier.mixins.mixins import NotLoggedInRequired
from cashier.profiles.forms import EditProfileForm
from cashier.profiles.models import UserProfile
from cashier.users.forms import UserForm

UserModel = get_user_model()

class HomeView(TemplateView):
	template_name = 'base/home_view.html'

class ContactView(TemplateView):
	template_name = 'base/contact_view.html'

class RegisterView(BootStrapFormMixin, NotLoggedInRequired, View):
	def get(self, request):
		user_form = UserForm()
		profile_form = EditProfileForm()
		context = {
			'user_form': user_form,
			'profile_form': profile_form,
		}
		self.apply_bootstrap_classes(user_form)
		self.apply_bootstrap_classes(profile_form)

		return render(request, 'users/register_view.html', context)

	def post(self, request):
		user_form = UserForm(request.POST)
		profile_form = EditProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			qwe = user.id
			user.id = request.user.id
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			login(request, user)
			return redirect('home_view')
		else:
			self.apply_bootstrap_classes(user_form)
			self.apply_bootstrap_classes(profile_form)
			context = {
				'user_form': user_form,
				'profile_form': profile_form,
			}
			return render(request, 'users/register_view.html', context)

class UserLoginView(BootStrapFormMixin, LoginView):
	template_name = 'users/login_view.html'
	redirect_authenticated_user = True