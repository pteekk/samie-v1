from rest_framework import serializers
from .models import Wallet, WalletMember, WalletInvitation
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

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




# Serializer for handling KYC check and validation
class KYCVerificationSerializer(serializers.Serializer):
    bvn = serializers.CharField(max_length=11)
    nin = serializers.CharField(max_length=20)
    card_number = serializers.CharField(max_length=19)
    expiry_month = serializers.CharField(max_length=2)
    expiry_year = serializers.CharField(max_length=4)
    cvv = serializers.CharField(max_length=4)

    def validate(self, attrs):
        # You can add more detailed BVN/NIN format validation here
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        user.bvn = validated_data['bvn']
        user.nin = validated_data['nin']
        # Simulate card tokenization — replace with real Paystack API call
        card_token = self.tokenize_card(validated_data)
        user.card_token = card_token
        user.save()
        return user

    def tokenize_card(self, card_data):
        # Replace this with actual Paystack call or helper
        # For now, just return a dummy token
        return f"TOKEN_{card_data['card_number'][-4:]}"
