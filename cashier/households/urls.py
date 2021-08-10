from django.urls import path

from cashier.households.views import household_profile_view, household_superuser_view, HouseholdEditProfileView, \
    HouseholdRemoveUser, HouseholdApproveUser, SetHouseholdAdmins, all_pending_members, urgent_pending_members

urlpatterns = [
    path('profile/<int:pk>', household_profile_view, name = 'hh_profile'),
    path('profile/<int:pk>/edit', HouseholdEditProfileView.as_view(), name="hh_profile_edit"),
    path('profile/<int:pk>/remove', HouseholdRemoveUser.as_view(), name="hh_profile_remove"),
    path('profile/<int:pk>/approve', HouseholdApproveUser.as_view(), name="hh_approve_user"),
    path('profile/<int:pk>/hh_admin', SetHouseholdAdmins.as_view(), name="set_hh_admin"),
    path('admin/', household_superuser_view, name = 'all_hh_profiles'),
    path('pending/all', all_pending_members, name = 'all_pending_members'),
    path('pending/urgent', urgent_pending_members, name = 'urgent_pending_members'),
]

