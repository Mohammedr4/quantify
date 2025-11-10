from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # This is our "pro" destination
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]
