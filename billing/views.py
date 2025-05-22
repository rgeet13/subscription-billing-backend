# billing/views.py

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from datetime import date
from .models import Plan, Subscription, Invoice
from .serializers import SubscriptionSerializer, InvoiceSerializer

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_name = request.data.get("plan")

        if not plan_name:
            return Response({"error": "Plan is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            return Response({"error": "Invalid plan."}, status=status.HTTP_400_BAD_REQUEST)

        # Cancel existing active subscription (optional logic)
        Subscription.objects.filter(user=request.user, status='active').update(status='cancelled')

        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=plan.billing_cycle_days)

        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status='active'
        )

        return Response({
            "message": "Subscribed successfully.",
            "subscription": {
                "plan": plan.name,
                "start_date": subscription.start_date,
                "end_date": subscription.end_date,
                "status": subscription.status,
            }
        }, status=status.HTTP_201_CREATED)


class UnsubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            subscription = Subscription.objects.get(user=user, status="active")
        except Subscription.DoesNotExist:
            return Response({"detail": "No active subscription found."}, status=status.HTTP_404_NOT_FOUND)

        subscription.status = "cancelled"
        subscription.end_date = date.today()
        subscription.save()

        serialized = SubscriptionSerializer(subscription)
        return Response({"detail": "Subscription cancelled.", "subscription": serialized.data}, status=status.HTTP_200_OK)

class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).order_by('-issue_date')


class InvoiceDetailView(generics.RetrieveAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

class PayInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        except Invoice.DoesNotExist:
            return Response({"detail": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)

        if invoice.status == "paid":
            return Response({"detail": "Invoice already paid."}, status=status.HTTP_400_BAD_REQUEST)

        invoice.status = "paid"
        invoice.paid_date = timezone.now()
        invoice.save()

        return Response({"detail": "Invoice marked as paid."}, status=status.HTTP_200_OK)