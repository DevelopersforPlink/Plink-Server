import ulid

from django.db import models

class BaseModel(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        default=lambda: str(ulid.ULID()),
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
