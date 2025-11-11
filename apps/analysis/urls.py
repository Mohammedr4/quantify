from django.urls import path
from . import views

app_name = "analysis"

urlpatterns = [
    path("tax-console/", views.TaxConsoleView.as_view(), name="tax_console"),
]