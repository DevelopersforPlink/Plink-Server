from django.conf import settings
from django.db import models
from common.models import BaseRequest
from users.models import Client, Manager
from pts.models import PT
from summits.models import Summit

class RequestStatus(models.TextChoices):
    PENDING = "PENDING", "대기중"
    APPROVED = "APPROVED", "승인됨"
    REJECTED = "REJECTED", "거절됨"

class PTRequest(BaseRequest):
    pt = models.ForeignKey(PT, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class SummitRequest(BaseRequest):
    summit = models.ForeignKey(Summit, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class ClientRequest(BaseRequest):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='managers')
