# billing/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
class Plan(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle_days = models.PositiveIntegerField(default=30)  # e.g., monthly

    def __str__(self):
        return self.get_name_display()

class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.email} - {self.status}"