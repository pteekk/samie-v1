from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    merchant_account_name = models.CharField(max_length=20)
    merchant_account_number = models.CharField(max_length=20)
    Description = models.CharField(max_length=500)
    disbursed = models.BooleanField(default=False)
    disbursement_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    lock_time = models.DateTimeField()  # FUTURE wallet opt-out window

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

@receiver(post_save, sender=WalletInvitation)
def prompt_kyc_after_acceptance(sender, instance, created, **kwargs):
    if not created and instance.accepted:
        user = instance.invited_user
        # Check if user lacks KYC
        if not (user.bvn and user.nin and user.card_token):
            # Flag the system or redirect logic will be done in views.
            print(f"KYC required for user {user.email}. Redirect to KYC page.")
            # You can set a flag on the user or send notification/email here