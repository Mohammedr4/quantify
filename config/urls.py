from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path("admin/", admin.site.urls),

    # "Pro" Auth
    path('accounts/', include('allauth.urls')), 

    # "Pro" Apps
    path("", include("apps.portfolios.urls")),
    path("", include("apps.users.urls")),
    path("", include("apps.calculators.urls")),

    # THIS IS THE "PRO" FIX:
    path("", include("apps.analysis.urls")), 
]