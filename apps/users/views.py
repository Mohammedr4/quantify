from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin  # <--- "Pro"
from django.views import View


class DashboardView(LoginRequiredMixin, View):
    """
    This is our "pro" "Empty State" Dashboard.
    It "outlaws" "slop" $0.00s and gives a "basics-first" CTA.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        # We "outlaw" "slop" logic for now. We just render the "pro" page.
        return render(request, "pages/dashboard.html")
