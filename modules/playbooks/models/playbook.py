from django.db import models

from modules.core.models import AuditFieldsMixin, Tag
from modules.core.models import Group
from modules.users.models import CustomUser


class Playbook(AuditFieldsMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    visible_to = models.ManyToManyField(
        Group,
        related_name='playbooks',
        blank=True,
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='playbook_tags',
        blank=True,
    )

    def is_visible_to(self, user: CustomUser):
        if self.is_public:
            return True
        if not user.is_authenticated:
            return False
        return self.visible_to.filter(id__in=user.get_user_group_ids()).exists()

    def __str__(self):
        return self.name
