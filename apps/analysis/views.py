from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from apps.portfolios.models import Portfolio
from .logic import calculate_cgt_summary

class TaxConsoleView(LoginRequiredMixin, View):
    """
    The "Pro" Tax Console.
    It runs the "Section 104" engine for every portfolio the user owns.
    """
    def get(self, request):
        user_portfolios = Portfolio.objects.filter(user=request.user)
        
        reports = []
        grand_total_gain = 0
        
        for portfolio in user_portfolios:
            # Run the "pro" engine we just tested
            summary = calculate_cgt_summary(portfolio)
            
            # Only show portfolios that actually have tax events
            if summary['taxable_events']:
                reports.append({
                    'portfolio_name': portfolio.name,
                    'events': summary['taxable_events'],
                    'total_gain': summary['total_gain']
                })
                grand_total_gain += summary['total_gain']

        context = {
            'reports': reports,
            'grand_total_gain': grand_total_gain
        }
        return render(request, "pages/tax_console.html", context)