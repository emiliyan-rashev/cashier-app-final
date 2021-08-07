from django.urls import path, include
from cashier.users.views import home_view, contact_view, register_view, login_view, logout_view

urlpatterns = [
	path('', home_view, name = 'home_view'),
	path('about/', contact_view, name = 'contact_view'),
	path('register/', register_view, name = 'register_view'),
	path('login/', login_view, name = 'login_view'),
	path('logout/', logout_view, name = 'logout_view'),
]

import cashier.users.signals