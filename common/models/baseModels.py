import ulid
from django.db import models
from common.models.baseModels import BaseModel
from .choiceModels import RequestStatus

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