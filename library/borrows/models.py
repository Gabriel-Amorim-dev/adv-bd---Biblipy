from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.apps import apps
from datetime import date


class Borrow(models.Model):

    STATUS_CHOICES = [
        ('pending', 'PENDING'),
        ('late', 'LATE'),
        ('returned', 'RETURNED'),
    ]

    user = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        related_name='borrows'
    )

    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='borrows'
    )

    borrow_date = models.DateField(auto_now_add=True)

    due_date = models.DateField()

    return_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.pk:  # Only for new borrows
            if self.book.quantity <= 0:
                raise ValidationError('This Book is unavailable.')

            active_borrows = Borrow.objects.filter(
                user=self.user,
                status__in=['pending', 'late']
            )

            if active_borrows.filter(book=self.book).exists():
                raise ValidationError('User already has this book borrowed.')

            if active_borrows.count() >= 3:
                raise ValidationError('User reached maximum borrow limit (3).')

    def save(self, *args, **kwargs):
        self.full_clean()

        is_new = self.pk is None

        with transaction.atomic():
            # Always fetch a fresh, locked copy of the book
            Book = apps.get_model('books', 'Book')
            locked_book = Book.objects.select_for_update().get(pk=self.book.pk)

            if is_new:
                locked_book.quantity -= 1
                locked_book.available = locked_book.quantity > 0
                locked_book.save()
            else:
                old_instance = Borrow.objects.select_for_update().get(pk=self.pk)
                if old_instance.status != 'returned' and self.status == 'returned':
                    locked_book.quantity += 1
                    locked_book.available = True
                    locked_book.save()
                    self.return_date = date.today()

            if self.due_date < date.today() and self.status != 'returned':
                self.status = 'late'

            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} - {self.book}'