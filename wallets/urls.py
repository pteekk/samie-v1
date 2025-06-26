from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, WalletMemberViewSet, WalletInvitationViewSet, KYCVerificationViewSet


router = DefaultRouter()
router.register('wallets', WalletViewSet)
router.register('wallet-members', WalletMemberViewSet)
router.register('wallet-invitation', WalletInvitationViewSet)
router.register(r'kyc', KYCVerificationViewSet, basename='kyc')



urlpatterns = [
    path('', include(router.urls)),
    path('kyc/verify/', KYCVerificationViewSet.as_view(), name='kyc_verification_page'),
]


