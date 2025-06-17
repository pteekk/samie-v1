from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Transaction
from .serializers import TransactionSerializer
from wallets.models import WalletMember
from .paystack import charge_authorization

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     @action(detail=False, methods=['post'])
#     def auto_debit_wallet_member(self, request):
#         member_id = request.data.get('wallet_member_id')
#         wallet_member = WalletMember.objects.get(id=member_id)

#         if not wallet_member.auto_debit_approved:
#             return Response({'error': 'Auto-debit not approved'}, status=status.HTTP_400_BAD_REQUEST)

#         user = wallet_member.user
#         amount_kobo = int(wallet_member.amount * 100)

#         result = charge_authorization(user.email, amount_kobo, user.card_token)

#         tx = Transaction.objects.create(
#             user=user,
#             wallet=wallet_member.wallet,
#             amount=wallet_member.amount,
#             status=result.get('status', 'pending'),
#             paystack_response=result
#         )

#         if result.get('status') == 'success':
#             wallet_member.contributed += wallet_member.amount
#             wallet_member.save()

#         return Response({'message': 'Auto-debit attempted.', 'paystack_result': result})



class TransactionListCreateView(generics.ListCreateAPIView):
    """
    List all transactions and create new transactions
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a transaction instance
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class AutoDebitWalletMemberView(APIView):
    """
    Handle auto-debit for wallet members
    """
    def post(self, request):
        member_id = request.data.get('wallet_member_id')
        
        try:
            wallet_member = WalletMember.objects.get(id=member_id)
        except WalletMember.DoesNotExist:
            return Response(
                {'error': 'Wallet member not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not wallet_member.auto_debit_approved:
            return Response(
                {'error': 'Auto-debit not approved'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = wallet_member.user
        amount_kobo = int(wallet_member.amount * 100)
        
        result = charge_authorization(user.email, amount_kobo, user.card_token)
        
        tx = Transaction.objects.create(
            user=user,
            wallet=wallet_member.wallet,
            amount=wallet_member.amount,
            status=result.get('status', 'pending'),
            paystack_response=result
        )
        
        if result.get('status') == 'success':
            wallet_member.contributed += wallet_member.amount
            wallet_member.save()
        
        return Response({
            'message': 'Auto-debit attempted.',
            'paystack_result': result,
            'transaction_id': tx.id
        })
