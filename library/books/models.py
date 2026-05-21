# books/models.py

from django.db import models


class Author(models.Model):

    name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=200)

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    publisher = models.CharField(max_length=150)

    publication_year = models.IntegerField()

    quantity = models.PositiveIntegerField(default=0)

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Shows newest books first
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return f"{self.title} ({self.quantity} unidades)"