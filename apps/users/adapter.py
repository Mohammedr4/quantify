from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        # "Pro" Fix: Force the username to be the email
        # This "outlaws" the empty username crash.
        user.username = user.email