from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    try:
        for overdue_loan in Loan.get_overdue_loans():
            send_mail(
                subject='Book Loaned Successfully',
                message=f'Hello {overdue_loan.member.user.username},\n\nYour loan is overdue."{overdue_loan.book.title}".\nPlease return it ASAP.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[overdue_loan.member.user.email],
                fail_silently=False,
            )
    except Exception:
        print("Exception")
