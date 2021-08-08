from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.views.generic import UpdateView

from cashier.households.models import HouseholdProfile
from cashier.profiles.forms import EditProfileForm
from cashier.profiles.models import UserProfile
from cashier.users.forms import UserForm, UserLoginForm

UserModel = get_user_model()

def home_view(request):
	return render(request, 'home_view.html')

def contact_view(request):
	if UserModel.objects.filter(is_superuser=True):
		superuser_id = UserModel.objects.filter(is_superuser=True).values_list('id')[0]
		superuser_email = UserProfile.objects.get(pk=superuser_id).email
		superuser_phone = UserProfile.objects.get(pk=superuser_id).phone_number
		superuser_first_name = UserProfile.objects.get(pk=superuser_id).first_name
		superuser_last_name = UserProfile.objects.get(pk=superuser_id).last_name
	else:
		superuser_email = 'default@email.com'
		superuser_phone = '0123456789'
		superuser_first_name = 'Default_First_Name'
		superuser_last_name = 'Default_Last_Name'
	context = {
		'phone_number' : superuser_phone,
		'e_mail' : superuser_email,
		'first_name' : superuser_first_name,
		'last_name' : superuser_last_name,
	}

	return render(request, 'contact_view.html', context)

def register_view(request):
	if request.method == 'POST':
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
			return redirect('home_view')
	else:
		user_form = UserForm()
		profile_form = EditProfileForm()

	context = {
		'user_form' : user_form,
		'profile_form' : profile_form,
	}
	return render(request, 'register_view.html', context)

def login_view(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home_view')
	else:
		form = UserLoginForm()

	context = {
		'user_form' : form,
	}

	return render(request, 'login_view.html', context)

def logout_view(request):
	logout(request)
	return redirect('home_view')

