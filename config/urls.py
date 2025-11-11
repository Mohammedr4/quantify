from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path("admin/", admin.site.urls),

    # This is our "pro" auth "steering wheel"
    path('accounts/', include('allauth.urls')), 

    # This is our "pro" "basics-first" routing.
    # It "outlaws" "slop" namespaces in the include.
    # The "pro" `app_name` in each app's `urls.py` handles this.
    path("", include("apps.portfolios.urls")),
    path("", include("apps.users.urls")),
    path("", include("apps.calculators.urls")),
]