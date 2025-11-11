from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from apps.marketdata.models import Stock

class Portfolio(TimeStampedModel):
    """
    This is the user's "pro" portfolio (e.g., "My ISA").
    A "pro" user (our CustomUser) can have *many* portfolios.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # This is the "pro" way
        on_delete=models.CASCADE,
        related_name="portfolios"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} (for {self.user.email})"

class Transaction(TimeStampedModel):
    """
    This is the "pro" "bulletproof" ledger.
    We "outlaw" "slop" (like "how many shares do you own?").
    We "pro" *force* the user to give us "basics-first" data.
    """
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    portfolio = models.ForeignKey(
        Portfolio, 
        on_delete=models.CASCADE, 
        related_name="transactions"
    )
    stock = models.ForeignKey(
        Stock, 
        on_delete=models.CASCADE, 
        related_name="transactions"
    )
    
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    
    # This is the "pro" "basics-first" data we "outlawed" "slop" for.
    date = models.DateField() 
    quantity = models.DecimalField(max_digits=19, decimal_places=8)
    price = models.DecimalField(max_digits=19, decimal_places=8) # Price *per share*
    fees = models.DecimalField(max_digits=19, decimal_places=8, default=0.00)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.stock.ticker} on {self.date}"