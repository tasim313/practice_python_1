from rest_framework import serializers
from .models import *


# class Customer_request_invoice_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = ('id', 'customer', 'service_provider', 'sub_category',
#                   'customer_address', 'customer_phone_number')


# class Service_Provider_Invoice_acceptance_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Invoice
#         fields = ('id', 'rate', 'number_of_units_of_time', 'transportation_cost',
#                   'cost_for_parts', 'tax_rate', 'service_provider_address', 'provider_phone_number', 'start_date', 'end_date', 'job_description', 'special_notes', 'invoice_status')


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
