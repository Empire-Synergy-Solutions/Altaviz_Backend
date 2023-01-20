from rest_framework import serializers
from core.serializers.user import UserSerializer
from fuelcredit.models.wallet import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Wallet
        fields = '__all__'
