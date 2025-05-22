

from django.urls import path
from .views import SubscribeView, UnsubscribeView, InvoiceListView, InvoiceDetailView, PayInvoiceView

urlpatterns = [
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("unsubscribe/", UnsubscribeView.as_view(), name="unsubscribe"),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:id>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path("invoices/<uuid:invoice_id>/pay/", PayInvoiceView.as_view(), name="pay-invoice"),
]
