from django.urls import path, include

from .views import TransactionListCreateView, TransactionDetailView, AutoDebitWalletMemberView


urlpatterns = [
    # Basic CRUD operations
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    
    # Auto-debit endpoint
    path('auto-debit/', AutoDebitWalletMemberView.as_view(), name='auto-debit-wallet-member'),
]
