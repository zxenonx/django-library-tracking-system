from datetime import timedelta

from django.dispatch import receiver
from django.db.signals import post_save
from .models import Loan

@receiver(post_save, sender=Loan)
def save_loaned_book(sender, instance, created, **kwargs):
    if created:
        instance.due_date = instance.loan_date + timedelta(days=14)
        instance.save()