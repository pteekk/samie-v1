from django.db import models
from django.conf import settings
from django.utils import timezone

class Wallet(models.Model):
    INSTANT = 'instant'
    FUTURE = 'future'
    WALLET_TYPES = [
        (INSTANT, 'Instant Expenses Wallet'),
        (FUTURE, 'Future/Planned Expenses Wallet'),
    ]

    name = models.CharField(max_length=255)
    wallet_type = models.CharField(max_length=10, choices=WALLET_TYPES)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    merchant_account_number = models.CharField(max_length=20)
    disbursed = models.BooleanField(default=False)
    disbursement_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lock_time = models.DateTimeField(blank=True, null=True)  # FUTURE wallet opt-out window

    def __str__(self):
        return self.name

class WalletMember(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    contributed = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    approved = models.BooleanField(default=False)
    auto_debit_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} in {self.wallet.name}'

class WalletInvitation(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_invitations', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Invitation to {self.invited_user.email} for {self.wallet.name}'
