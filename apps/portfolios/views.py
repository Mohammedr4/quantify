from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Portfolio, Transaction
from apps.marketdata.models import Stock, DailyStockPrice
import yfinance as yf
import logging

# "Pro" logging setup
logger = logging.getLogger(__name__)

#
# 1. "PRO" PORTFOLIO VIEW
#
class PortfolioCreateView(LoginRequiredMixin, CreateView):
    """
    This is our "pro" "basics-first" view to create a Portfolio.
    """
    model = Portfolio
    template_name = "pages/portfolio_form.html"
    fields = ['name']
    
    success_url = reverse_lazy("portfolios:transaction_add") 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#
# 2. "PRO" TRANSACTION VIEW
#
class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    This is our "pro" "basics-first" view to create a Transaction.
    """
    model = Transaction
    template_name = "pages/transaction_form.html"
    
    # "PRO" FIX #1: We "outlaw" 'stock' from this list.
    # The form will no longer check for it. We set it manually in form_valid.
    fields = ['portfolio', 'transaction_type', 'date', 'quantity', 'price', 'fees']

    success_url = reverse_lazy("users:dashboard") 

    def get_context_data(self, **kwargs):
        """
        "Pro" context to filter portfolios.
        """
        context = super().get_context_data(**kwargs)
        
        # "PRO" FIX #2: We removed the code hiding 'stock' widget 
        # because 'stock' is no longer in the form fields.
        
        if 'form' in context:
            # "Pro" Fix: Filter the portfolio list to *only* this user.
            user_portfolios = Portfolio.objects.filter(user=self.request.user)
            context['form'].fields['portfolio'].queryset = user_portfolios
        
        return context

    def form_valid(self, form):
        """
        This is our "bulletproof" logic.
        We manually find the stock and attach it BEFORE saving.
        """
        # 1. "Pro" Stock check:
        ticker = self.request.POST.get('ticker', '').upper().strip()
        if not ticker:
            form.add_error(None, "Ticker is a 'bulletproof' requirement.")
            return self.form_invalid(form)

        # 2. "Pro" "Get or Create" logic:
        # We find the stock here and attach it to the instance
        stock, created = Stock.objects.get_or_create(ticker=ticker)
        form.instance.stock = stock
        
        # 3. "Pro" Portfolio Check:
        portfolio_id = self.request.POST.get('portfolio')
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id, user=self.request.user)
            form.instance.portfolio = portfolio
        except Portfolio.DoesNotExist:
            form.add_error('portfolio', "This is 'slop'. Select a 'pro' portfolio.")
            return self.form_invalid(form)

        # ---
        # "PRO" SYNC ENGINE (No Celery)
        # ---
        self.fetch_stock_data_sync(ticker)

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        "Pro" Debugger
        """
        print("--------------------------------------------------")
        print("❌ 'SLOP' FORM INVALID! 'PRO' ERRORS:")
        print(form.errors)
        print("--------------------------------------------------")
        return super().form_invalid(form)

    def fetch_stock_data_sync(self, ticker):
        """
        "Pro" Synchronous EOD Engine
        """
        try:
            stock = Stock.objects.get(ticker=ticker)
            ticker_data = yf.Ticker(ticker)
            
            # "Pro" data fill
            info = ticker_data.info
            if not stock.company_name and info:
                stock.company_name = info.get('longName', ticker)
                stock.save()
            
            hist = ticker_data.history(period='1d')
            
            if not hist.empty:
                latest_price = hist['Close'].iloc[-1]
                latest_date = hist.index[-1].date()
                
                DailyStockPrice.objects.update_or_create(
                    stock=stock,
                    date=latest_date,
                    defaults={'price': latest_price}
                )
                logger.info(f"Pro' SYNC update for {ticker}: {latest_price} on {latest_date}")
            else:
                logger.warning(f"'Slop' data: No history found for {ticker}")

        except Exception as e:
            logger.error(f"FATAL 'slop' SYNC error fetching {ticker}: {e}")