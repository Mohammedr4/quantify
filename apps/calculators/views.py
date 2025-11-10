from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def landing_page(request: HttpRequest) -> HttpResponse:
    """
    This is our "pro" landing page, User Story #1.
    It handles both the "Guest" page load (GET) and
    the "pro" HTMX calculation (POST).
    """

    # "Slop" check: We "outlaw" "mediocre" logic.
    if request.method == "POST":
        # This is the "pro" HTMX request.
        try:
            # 1. Get "pro" data from the HTMX form
            shares_held = float(request.POST.get("shares_held", 0))
            avg_price = float(request.POST.get("avg_price", 0))
            market_price = float(request.POST.get("market_price", 0))
            shares_to_buy = float(request.POST.get("shares_to_buy", 0))

            # 2. Run the "bulletproof" math
            current_cost = shares_held * avg_price
            new_cost = shares_to_buy * market_price
            total_shares = shares_held + shares_to_buy

            # "Anti-slop" check: We "outlaw" division by zero.
            if total_shares == 0:
                new_avg_price = 0.0
                total_investment = 0.0
            else:
                total_investment = current_cost + new_cost
                new_avg_price = total_investment / total_shares

            context = {
                "new_avg_price": new_avg_price,
                "total_shares": total_shares,
                "total_investment": total_investment,
            }

            # 3. Return the "pro" HTMX partial template
            # This is the "non-slop" magic. We "outlaw" full page reloads.
            return render(request, "partials/_reprice_results.html", context)

        except (ValueError, TypeError):
            # "Pro" error handling for "slop" input
            return HttpResponse("Invalid input.", status=400)

    # This is the "basics-first" GET request (the first page load)
    return render(request, "pages/landing_page.html")
