from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import (
    HomeView,
    ContactView,
    RegisterView,
    UserLoginView,
    EditContactView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home_view"),
    path("about/", ContactView.as_view(), name="contact_view"),
    path("about/update", EditContactView.as_view(), name="update_contact_view"),
    path("register/", RegisterView.as_view(), name="register_view"),
    path("login/", UserLoginView.as_view(), name="login_view"),
    path("logout/", LogoutView.as_view(), name="logout_view"),
]

