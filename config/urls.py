from django.contrib import admin
from django.urls import path, include  # <--- This is "pro"

urlpatterns = [
    path("admin/", admin.site.urls),
    # This is the "pro" hook for User Story #1.
    # It makes our "calculators" app the "pro" homepage.
    path("", include("apps.calculators.urls", namespace="calculators")),
]
