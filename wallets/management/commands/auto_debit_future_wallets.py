from django.core.management.base import BaseCommand
from wallets.models import Wallet, WalletMember
from transactions.paystack import charge_authorization
from transactions.models import Transaction
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Auto-debit members of future/planned wallets'

    def handle(self, *args, **options):
        future_wallets = Wallet.objects.filter(wallet_type=Wallet.FUTURE, disbursed=False, disbursement_date__gte=now())

        for wallet in future_wallets:
            members = wallet.members.filter(approved=True, auto_debit_approved=True)
            for member in members:
                remaining_amount = member.amount - member.contributed
                if remaining_amount > 0:
                    amount_kobo = int(remaining_amount * 100)
                    result = charge_authorization(member.user.email, amount_kobo, member.user.card_token)

                    Transaction.objects.create(
                        user=member.user,
                        wallet=wallet,
                        amount=remaining_amount,
                        status=result.get('status', 'pending'),
                        paystack_response=result
                    )

                    if result.get('status') == 'success':
                        member.contributed += remaining_amount
                        member.save()

        self.stdout.write(self.style.SUCCESS('Auto-debit process completed.'))


# python manage.py auto_debit_future_wallets
