from .models import *
from rest_framework import serializers


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = ('__all__')


class CreditCardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardInfo
        fields = ('__all__')


class BilingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = ('__all__')