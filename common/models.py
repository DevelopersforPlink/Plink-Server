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

class RequestStatus(models.TextChoices):
    PENDING = "PENDING", "대기중"
    APPROVED = "APPROVED", "승인됨"
    REJECTED = "REJECTED", "거절됨"

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

class BusinessProgressChoices(models.TextChoices):
    IDEA = "IDEA", "아이디어"
    IN_PROGRESS = "IN_PROGRESS", "사업 진행중"

class BusinessTypeChoices(models.TextChoices):
    SERVICE = "SERVICE", "서비스업"
    FINANCE = "FINANCE", "금융/은행업"
    IT = "IT", "IT/정보통신업"
    RETAIL = "RETAIL", "판매/유통업"
    MANUFACTURING = "MANUFACTURING", "제조/생산/화학업"
    EDUCATION = "EDUCATION", "교육업"
    CONSTRUCTION = "CONSTRUCTION", "건설업"
    MEDICAL = "MEDICAL", "의료/제약업"
    MEDIA = "MEDIA", "미디어/광고업"
    CULTURE = "CULTURE", "문화/예술/디자인업"