import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class Member(AbstractUser):
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Matrícula",
        editable=True
    )

    def save(self, *args, **kwargs):
        if not self.registration_number:
            self.registration_number = get_random_string(10, allowed_chars=string.ascii_uppercase + string.digits)
        super().save(*args, **kwargs)

    phone = models.CharField(max_length=20, verbose_name="Telefone")

    full_name = models.CharField(max_length=150)

    def __str__(self):
        return self.username