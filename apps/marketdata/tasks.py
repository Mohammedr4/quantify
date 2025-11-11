from celery import shared_task
import yfinance as yf
from .models import Stock, DailyStockPrice
import logging

# "Pro" "non-slop" logging
logger = logging.getLogger(__name__)

@shared_task(name="fetch_stock_data")
def fetch_stock_data(ticker):
    """
    This is our "pro" "basics-first" EOD Engine.
    It "outlaws" "slop" APIs and uses "pro" yfinance.
    """
    try:
        # 1. "Pro" "Get or Create" the stock
        stock, created = Stock.objects.get_or_create(ticker=ticker)
        if created:
            logger.info(f"Created new 'pro' stock: {ticker}")

        # 2. Get the "pro" data
        ticker_data = yf.Ticker(ticker)

        # 3. "Pro" update of the name (in case it was "slop")
        if not stock.company_name:
            stock.company_name = ticker_data.info.get('longName', ticker)
            stock.save()

        # 4. Get the "pro" EOD price
        # We use '1d' to "outlaw" "slop" real-time data
        hist = ticker_data.history(period='1d')

        if not hist.empty:
            latest_price = hist['Close'].iloc[-1]
            latest_date = hist.index[-1].date()

            # 5. "Pro" "Update or Create" the "bulletproof" price
            DailyStockPrice.objects.update_or_create(
                stock=stock,
                date=latest_date,
                defaults={'price': latest_price}
            )
            logger.info(f"Pro' update for {ticker}: {latest_price} on {latest_date}")
        else:
            logger.warning(f"'Slop' data: No history found for {ticker}")

    except Exception as e:
        # "Bulletproof" "non-slop" error handling
        logger.error(f"FATAL 'slop' error fetching {ticker}: {e}")