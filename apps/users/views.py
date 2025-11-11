from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Sum, F
from apps.portfolios.models import Portfolio, Transaction
from apps.marketdata.models import DailyStockPrice

class DashboardView(LoginRequiredMixin, View):
    """
    This is our "pro" Dashboard Engine.
    It switches between "Empty State" and "Full Dashboard" based on data.
    """
    def get(self, request):
        user = request.user
        
        # 1. Get the "pro" data
        portfolios = Portfolio.objects.filter(user=user)
        transactions = Transaction.objects.filter(portfolio__user=user).order_by('-date')
        
        # 2. The "Pro" Switch
        # If they have no transactions, show the "Empty State"
        if not transactions.exists():
            return render(request, "pages/dashboard.html", {'user': user})

        # 3. Calculate the "Big Number" (Total Cost Basis for now)
        # We will upgrade this to "Market Value" once our EOD engine runs fully.
        total_invested = 0
        for t in transactions:
            if t.transaction_type == 'BUY':
                total_invested += (t.quantity * t.price) + t.fees
            elif t.transaction_type == 'SELL':
                total_invested -= (t.quantity * t.price) # Simplified "pro" logic

        context = {
            'user': user,
            'portfolios': portfolios,
            'recent_transactions': transactions[:5], # Show last 5
            'total_net_worth': total_invested, # "Pro" placeholder for Cost Basis
        }
        
        # 4. Render the "Full" Dashboard
        return render(request, "pages/dashboard_full.html", context)