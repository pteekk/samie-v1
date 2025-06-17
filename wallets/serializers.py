from rest_framework import serializers
from .models import Wallet, WalletMember, WalletInvitation

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class WalletMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletMember
        fields = '__all__'

class WalletInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletInvitation
        fields = '__all__'
