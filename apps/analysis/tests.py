from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.portfolios.models import Portfolio, Transaction
from apps.marketdata.models import Stock
from .logic import calculate_cgt_summary  # We haven't built this yet. That's "Pro".
from datetime import date
from decimal import Decimal

User = get_user_model()

class UKTaxTests(TestCase):
    def setUp(self):
        # "Pro" Setup: Create User, Portfolio, Stock
        self.user = User.objects.create_user(username='testuser', email='test@pro.com', password='password')
        self.portfolio = Portfolio.objects.create(user=self.user, name="Test Portfolio")
        self.stock = Stock.objects.create(ticker="AAPL", company_name="Apple")

    def test_section_104_pool_calculation(self):
        """
        "Pro" Test: Verify UK Section 104 (Average Cost) Logic.
        Scenario:
        1. Buy 10 @ £100 (Cost: £1000)
        2. Buy 10 @ £120 (Cost: £1200)
           -> POOL: 20 shares, Total Cost £2200, Avg Cost £110.
        3. Sell 5 @ £150 (Proceeds: £750)
           -> COST OF SOLD: 5 * £110 = £550
           -> GAIN: £750 - £550 = £200.
        """
        
        # Transaction 1: Buy 10 @ 100
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock, transaction_type='BUY',
            date=date(2023, 1, 1), quantity=10, price=100, fees=0
        )

        # Transaction 2: Buy 10 @ 120
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock, transaction_type='BUY',
            date=date(2023, 1, 2), quantity=10, price=120, fees=0
        )

        # Transaction 3: Sell 5 @ 150
        # This is the one we need to calculate the Tax on.
        Transaction.objects.create(
            portfolio=self.portfolio, stock=self.stock, transaction_type='SELL',
            date=date(2023, 1, 10), quantity=5, price=150, fees=0
        )

        # --- THE "PRO" EXECUTION ---
        # We call our future logic function
        report = calculate_cgt_summary(self.portfolio)

        # --- THE "BULLETPROOF" ASSERTIONS ---
        # We expect to find 1 "Taxable Event" (The Sell)
        self.assertEqual(len(report['taxable_events']), 1)
        
        event = report['taxable_events'][0]
        
        # Check the math (using strings to avoid float "slop")
        self.assertEqual(event['ticker'], "AAPL")
        self.assertEqual(event['gain'], Decimal('200.00')) # £750 proceeds - £550 cost
        self.assertEqual(event['pool_remaining_qty'], Decimal('15.00'))
        self.assertEqual(event['pool_remaining_cost'], Decimal('1650.00')) # £2200 - £550