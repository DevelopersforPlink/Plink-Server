import ulid
from django.db import models
from .choiceModels import RequestStatus
from common.utils.requestIDGenerator import generate_request_id

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
    request_id = models.CharField(max_length=12, unique=True, editable=False)  # 요청번호 필드 추가
    requested_at = models.DateField(auto_now_add=True)
    reject_reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.request_id:
            self.request_id = generate_request_id(self.get_request_type())
        super().save(*args, **kwargs)
    
    def get_category(self) -> str:
        request_type = self.get_request_type()
        category_mapping = {
            "UVR": "회원 승인 요청",
            "PSR": "프레젠테이션 승인 요청",
            "SSR": "써밋 생성 승인 요청"
        }
        return category_mapping.get(request_type, "기타 요청")

    def get_request_type(self) -> str:
        raise NotImplementedError("Subclass must implement `get_request_type` method.")