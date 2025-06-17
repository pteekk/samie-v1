from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Wallet, WalletMember, WalletInvitation
from .serializers import WalletSerializer, WalletMemberSerializer, WalletInvitationSerializer
from transactions.paystack import transfer_to_bank
from notifications.firebase_utils import send_push_notification

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=['post'])
    def disburse(self, request, pk=None):
        wallet = self.get_object()
        members = wallet.members.filter(approved=True, contributed__gte=models.F('amount'))
        total_contributed = sum([m.contributed for m in members])
        amount_kobo = int(total_contributed * 100)

        # For FUTURE wallet, enforce all members must contribute fully
        if wallet.wallet_type == Wallet.FUTURE:
            if members.count() != wallet.members.count():
                return Response({'error': 'Not all members have contributed fully.'}, status=status.HTTP_400_BAD_REQUEST)

        paystack_result = transfer_to_bank(wallet.merchant_account_number, amount_kobo)

        wallet.disbursed = True
        wallet.disbursement_date = timezone.now()
        wallet.save()

        # Notify members
        for member in members:
            send_push_notification(member.user.firebase_token, f'Wallet {wallet.name} has been disbursed.')

        return Response({'message': 'Funds disbursed to merchant.', 'paystack_result': paystack_result})

class WalletMemberViewSet(viewsets.ModelViewSet):
    queryset = WalletMember.objects.all()
    serializer_class = WalletMemberSerializer

class WalletInvitationViewSet(viewsets.ModelViewSet):
    queryset = WalletInvitation.objects.all()
    serializer_class = WalletInvitationSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if invitation.accepted:
            return Response({'message': 'Already accepted'}, status=status.HTTP_400_BAD_REQUEST)
        
        invitation.accepted = True
        invitation.save()

        WalletMember.objects.create(
            wallet=invitation.wallet,
            user=invitation.invited_user,
            amount=0.0,
            approved=False
        )

        # Notify creator
        send_push_notification(invitation.invited_by.firebase_token, f'{invitation.invited_user.email} accepted your wallet invitation.')

        return Response({'message': 'Invitation accepted and wallet membership created.'})
