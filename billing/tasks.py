from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Invoice

@shared_task
def generate_invoices():
    today = timezone.now().date()
    subscriptions = Subscription.objects.filter(status='active', start_date__lte=today)

    for sub in subscriptions:
        Invoice.objects.create(
            user=sub.user,
            subscription=sub,
            plan=sub.plan,
            amount=sub.plan.price,
            issue_date=today,
            due_date=today + timedelta(days=7),
            status='pending'
        )
    return f"{subscriptions.count()} invoices generated."

@shared_task
def mark_overdue_invoices():
    overdue_invoices = Invoice.objects.filter(status='pending', due_date__lt=timezone.now())
    count = overdue_invoices.update(status='overdue')
    print(f"[Overdue Task] Marked {count} invoices as overdue.")