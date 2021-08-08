from django.urls import path

from cashier.households.views import HouseholdProfileView, HouseholdAdminView, HouseholdEditProfileView, \
    HouseholdRemoveUser, HouseholdApproveUser

urlpatterns = [
    path('profile/<int:pk>', HouseholdProfileView, name = 'hh_profile'),
    path('profile/<int:pk>/edit', HouseholdEditProfileView.as_view(), name="hh_profile_edit"),
    path('profile/<int:pk>/remove', HouseholdRemoveUser.as_view(), name="hh_profile_remove"),
    path('profile/<int:pk>/approve', HouseholdApproveUser.as_view(), name="hh_approve_user"),
    path('admin/', HouseholdAdminView, name = 'all_hh_profiles'),
]

