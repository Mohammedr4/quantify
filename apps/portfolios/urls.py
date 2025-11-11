from django.urls import path
from . import views

app_name = "portfolios"

urlpatterns = [
    # This is our "pro" "basics-first" step
    path(
        "portfolio/add/", 
        views.PortfolioCreateView.as_view(), 
        name="portfolio_add"
    ),

    # This is our "pro" "steering wheel" that fixes the "slop" crash
    path(
        "transaction/add/", 
        views.TransactionCreateView.as_view(), 
        name="transaction_add"
    ),
]