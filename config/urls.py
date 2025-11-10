from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # This is our "pro" auth "steering wheel"
    path("accounts/", include("allauth.urls")),
    # This is our "pro" "Empty State" Dashboard hook
    path("", include("apps.users.urls", namespace="users")),
    # This is our "pro" "Guest" hook (ONCE. "Outlaw" "slop" duplicates.)
    path("", include("apps.calculators.urls", namespace="calculators")),
]
