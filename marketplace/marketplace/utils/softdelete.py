from django.db import models
from django.utils import timezone
from django.db.utils import OperationalError
from django.core.exceptions import FieldError


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        # Only apply the is_active filter if the model actually has that field.
        # Calling .filter(...) would not hit the DB immediately; the SQL executes
        # later and would raise if the column is missing. Inspect model metadata
        # to avoid generating SQL that references a non-existent column.
        # Use DB introspection to confirm the column exists in the actual table.
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                try:
                    desc = connection.introspection.get_table_description(cursor, self.model._meta.db_table)
                except Exception:
                    # table might not exist yet or introspection unsupported
                    return qs
            column_names = [col.name for col in desc]
            if 'is_active' in column_names:
                return qs.filter(is_active=True)
            return qs
        except Exception:
            # conservative fallback: return unfiltered queryset to avoid startup crash
            return qs


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_active', 'deleted_at'])

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=['is_active', 'deleted_at'])
