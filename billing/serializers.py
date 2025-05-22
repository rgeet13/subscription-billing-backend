from rest_framework import serializers
from .models import Subscription, Invoice

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'status']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'user', 'plan', 'amount', 'issue_date', 'due_date', 'status']
        read_only_fields = fields
