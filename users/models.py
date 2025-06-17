from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nin = models.CharField(max_length=20, blank=True, null=True)
    bvn = models.CharField(max_length=11, blank=True, null=True)
    card_token = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=10, blank=True, null=True)
    bank_code = models.CharField(max_length=10, blank=True, null=True)
    is_kyc_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
