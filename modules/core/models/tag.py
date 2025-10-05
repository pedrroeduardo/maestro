from django.db import models

from modules.core.models import AuditFieldsMixin


class Tag(AuditFieldsMixin):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name