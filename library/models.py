from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-Fiction'),
        ('sci-fi', 'Sci-Fi'),
        ('biography', 'Biography'),
        # Add more genres as needed
    ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_date = models.DateField(auto_now_add=True)
    # Add more fields if necessary

    def __str__(self):
        return self.user.username

class Loan(models.Model):
    book = models.ForeignKey(Book, related_name='loans', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='loans', on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} loaned to {self.member.user.username}"

    def is_overdue(self):
        return not self.is_returned and (self.due_date < date.today())

    def extend_due_date(self, additional_days: int):
        self.due_date += timedelta(days=additional_days)
        return self

    @staticmethod
    def get_overdue_loans():
        return Loan.objects.filter(is_returned=False, due_date__lt=date.today())
