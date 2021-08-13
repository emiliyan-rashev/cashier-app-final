from django.shortcuts import render
from django.urls import path

from cashier.profiles.views import EditProfileView, DeleteProfileView, ViewProfileView, ShowAllUsersView

urlpatterns = [
    path('edit/<int:pk>', EditProfileView.as_view(), name = 'edit_profile'),
    path('delete/<int:pk>', DeleteProfileView.as_view(), name = 'delete_profile'),
    path('view/<int:pk>', ViewProfileView.as_view(), name = 'view_profile'),
    path('all/', ShowAllUsersView.as_view(), name='all_users')
]

import cashier.profiles.signals