import ulid
from django.db import models
from .choiceModels import RequestStatus

def generate_ulid():
    return str(ulid.ULID())

class BaseModel(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        default=generate_ulid,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseRequest(BaseModel):
    requested_at = models.DateTimeField(auto_now_add=True)
    reject_reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )

    class Meta:
        abstract = True