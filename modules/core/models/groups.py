from django.conf import settings
from django.db import models
from modules.core.models import AuditFieldsMixin

class Group(AuditFieldsMixin):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='GroupMember',
        through_fields=('group', 'user'),
        related_name='maestro_groups',
        related_query_name='maestro_group',
        blank=True,
    )

    def __str__(self):
        return self.name

class GroupMember(AuditFieldsMixin):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'user'], name='unique_group_user')
        ]

    def __str__(self):
        return f"{self.user} in {self.group}"
