from django.urls import path
from . import views

# We "outlaw" "slop" naming.
app_name = "calculators"

urlpatterns = [
    # This is User Story #1. The "pro" landing page.
    path("", views.landing_page, name="landing"),
]
