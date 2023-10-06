from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("profile/", include("profiles.urls")),
    path("household/", include("households.urls")),
    path("payments/", include("payments.urls")),
    path("news/", include("news.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
