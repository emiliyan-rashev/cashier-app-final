from django.urls import path

from cashier.households.views import HouseholdEditProfileView, HouseholdRemoveUser, HouseholdApproveUser, \
    SetHouseholdAdmins, HouseholdProfileView, AllPendingMembersView, UrgentPendingMembersView, HouseholdSuperuserView, \
    HouseHoldMemberPaymentsView

urlpatterns = [
    path('profile/<int:pk>', HouseholdProfileView.as_view(), name = 'hh_profile'),
    path('profile/<int:pk>/edit', HouseholdEditProfileView.as_view(), name="hh_profile_edit"),
    path('profile/<int:pk>/remove', HouseholdRemoveUser.as_view(), name="hh_profile_remove"),
    path('profile/<int:pk>/approve', HouseholdApproveUser.as_view(), name="hh_approve_user"),
    path('profile/<int:pk>/hh_admin', SetHouseholdAdmins.as_view(), name="set_hh_admin"),
    path('admin/', HouseholdSuperuserView.as_view(), name = 'all_hh_profiles'),
    path('pending/all', AllPendingMembersView.as_view(), name = 'all_pending_members'),
    path('pending/urgent', UrgentPendingMembersView.as_view(), name = 'urgent_pending_members'),
    path('<int:pk>/members/payments', HouseHoldMemberPaymentsView.as_view(), name = 'hh_member_payment'),
]

