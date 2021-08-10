from django.shortcuts import render
from django.urls import path

from cashier.profiles.views import EditProfileView, DeleteProfileView, ViewProfileView, confirm_delete

urlpatterns = [
    path('edit/', EditProfileView.as_view(), name = 'edit_profile'),
    path('delete/<int:pk>', confirm_delete, name = 'delete_profile'),
    path('view/<int:pk>', ViewProfileView, name = 'view_profile'),
]

import cashier.profiles.signals