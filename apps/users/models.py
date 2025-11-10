from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    This is our "pro" user model.
    We are "outlawing" the "slop" default model.
    """
    email = models.EmailField(unique=True)

    # We will add our "pro" fields here later:
    # primary_currency = models.CharField(max_length=3, default='GBP')
    # tax_jurisdiction = models.CharField(max_length=2, default='UK')

    def __str__(self):
        return self.username