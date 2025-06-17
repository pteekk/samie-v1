from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WalletViewSet, WalletMemberViewSet
from .views import WalletInvitationViewSet


router = DefaultRouter()
router.register('wallets', WalletViewSet)
router.register('wallet-members', WalletMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



# Add Invitation Route
router.register('wallet-invitations', WalletInvitationViewSet)
