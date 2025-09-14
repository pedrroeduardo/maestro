from .audit_fields_mixin import AuditFieldsMixin

class AuditModel(AuditFieldsMixin):
    class Meta:
        abstract = True