from django.contrib.auth.models import AbstractUser
from django.db import models
from modules.core.models.audit_fields_mixin import AuditFieldsMixin

class CustomUser(AbstractUser, AuditFieldsMixin):
    email = models.EmailField(unique=True)

    address = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    postal_code = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    state = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    language = models.CharField(max_length=50, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.email