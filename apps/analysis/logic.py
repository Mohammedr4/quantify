from decimal import Decimal
from apps.portfolios.models import Transaction

def calculate_cgt_summary(portfolio):
    """
    "Pro" UK Tax Engine (Section 104 Pool).
    Iterates through transactions to calculate Realized Gains/Losses.
    """
    # 1. Get all transactions sorted by date (Crucial for the Pool)
    transactions = Transaction.objects.filter(portfolio=portfolio).order_by('date')

    # The "Section 104" Pool State
    # We track this per-stock
    pools = {} 
    taxable_events = []
    total_gain = Decimal('0.00')

    for t in transactions:
        ticker = t.stock.ticker

        # Initialize pool for this stock if new
        if ticker not in pools:
            pools[ticker] = {
                'quantity': Decimal('0.00'),
                'total_cost': Decimal('0.00')
            }

        pool = pools[ticker]

        if t.transaction_type == 'BUY':
            # ADD to the pool
            # Logic: New Total Cost = Old Total Cost + (Price * Qty) + Fees
            cost_of_buy = (t.price * t.quantity) + t.fees
            pool['quantity'] += t.quantity
            pool['total_cost'] += cost_of_buy

        elif t.transaction_type == 'SELL':
            # CALCULATE GAIN based on the pool's *current* average
            if pool['quantity'] > 0:
                # 1. Calculate Average Cost Per Share (The "Section 104" Price)
                avg_cost_per_share = pool['total_cost'] / pool['quantity']

                # 2. Determine Cost Basis for THIS sale
                # (This amount leaves the pool)
                cost_basis_of_sale = avg_cost_per_share * t.quantity

                # 3. Calculate Proceeds
                proceeds = (t.price * t.quantity) - t.fees

                # 4. Calculate Gain/Loss
                gain = proceeds - cost_basis_of_sale

                # 5. Update the Pool (Remove the shares and the cost)
                pool['quantity'] -= t.quantity
                pool['total_cost'] -= cost_basis_of_sale

                # 6. Log the "Taxable Event"
                taxable_events.append({
                    'date': t.date,
                    'ticker': ticker,
                    'quantity': t.quantity,
                    'proceeds': proceeds,
                    'cost_basis': cost_basis_of_sale,
                    'gain': gain,
                    'pool_remaining_qty': pool['quantity'],
                    'pool_remaining_cost': pool['total_cost']
                })

                total_gain += gain

    return {
        'taxable_events': taxable_events,
        'total_gain': total_gain
    }