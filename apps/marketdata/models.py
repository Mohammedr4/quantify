from django.db import models
from django_extensions.db.models import TimeStampedModel

class Stock(TimeStampedModel):
    """
    This is our "pro" model for a unique asset.
    It "outlaws" "slop" (like saving the price here).
    It is "basics-first": What *is* this asset?
    """
    ticker = models.CharField(max_length=20, unique=True, db_index=True)
    company_name = models.CharField(max_length=255, blank=True)
    # "Pro" type: 'STOCK', 'CRYPTO', 'ETF'
    asset_type = models.CharField(max_length=20, default='STOCK')

    def __str__(self):
        return f"{self.ticker} ({self.company_name})"

class DailyStockPrice(TimeStampedModel):
    """
    This is our "pro" EOD price ledger.
    Our "bulletproof" Celery engine will "pro" fill this table.
    It "outlaws" "slop" real-time APIs.
    """
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField(db_index=True)
    
    # We use "pro" DecimalFields for "non-slop" money.
    price = models.DecimalField(max_digits=19, decimal_places=8)
    
    # We must "outlaw" "slop" duplicates. One price per day.
    class Meta:
        unique_together = ('stock', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.stock.ticker} on {self.date}: {self.price}"
