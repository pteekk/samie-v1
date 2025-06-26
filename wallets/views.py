from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Wallet, WalletMember, WalletInvitation
from .serializers import WalletSerializer, WalletMemberSerializer, WalletInvitationSerializer, KYCVerificationSerializer
from transactions.paystack import transfer_to_bank
from notifications.firebase_utils import send_push_notification

from rest_framework.permissions import IsAuthenticated


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

        # Added for checking and redirecting for KYC 22/6/25
        if not (user.bvn and user.nin and user.card_token):
            return redirect('kyc_verification_page')  # Define this route in your urls

        WalletMember.objects.create(
            wallet=invitation.wallet,
            user=invitation.invited_user,
            amount=0.0,
            approved=False
        )

        # Notify creator
        send_push_notification(invitation.invited_by.firebase_token, f'{invitation.invited_user.email} accepted your wallet invitation.')

        return Response({'message': 'Invitation accepted and wallet membership created.'})


# View for handling KYC check and validation
# class KYCVerificationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Optional: Prefill existing data"""
#         user = request.user
#         data = {
#             "bvn": user.bvn or "",
#             "nin": user.nin or "",
#         }
#         return Response(data)

#     def post(self, request):
#         serializer = KYCVerificationSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "KYC completed successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KYCVerificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def verify(self, request, pk=None):
        """Optional: Prefill existing data"""
        user = request.user
        data = {
            "bvn": user.bvn or "",
            "nin": user.nin or "",
        }
        return Response(data)

    @action(detail=False, methods=['post'])
    def submit(self, request):
        serializer = KYCVerificationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "KYC completed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)