from django.conf import settings
from django.db import models
from common.models import BaseModel, BusinessTypeChoices, BusinessProgressChoices
from users.models import Client
from summits.models import Summit

class PT(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pts')
    summit = models.ForeignKey(Summit, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='')
    link = models.URLField()
    total_link = models.URLField()
    summary = models.TextField()
    summary_business_plan  = models.FileField(upload_to='')
    business_plan = models.FileField(upload_to='')
    pitch_deck = models.FileField(upload_to='')
    traction_data = models.FileField(upload_to='')
    business_type = models.CharField(
        max_length=20,
        choices=BusinessTypeChoices.choices,
        default=BusinessTypeChoices.SERVICE
    )
    business_progress= models.CharField(
        max_length=20,
        choices=BusinessProgressChoices.choices,
        default=BusinessProgressChoices.IDEA
    )
    is_summit = models.BooleanField(default=False)