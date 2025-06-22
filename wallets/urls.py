from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, WalletMemberViewSet, WalletInvitationViewSet, KYCVerificationView


router = DefaultRouter()
router.register('wallets', WalletViewSet)
router.register('wallet-members', WalletMemberViewSet)
router.register('wallet-invitation', WalletInvitationViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('kyc/verify/', KYCVerificationView.as_view(), name='kyc_verification_page'),
]



# Add Invitation Route
router.register('wallet-invitations', WalletInvitationViewSet)
