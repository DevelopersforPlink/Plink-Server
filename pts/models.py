from django.db import models
from common.models.choiceModels import BusinessProgressChoices, BusinessTypeChoices
from users.models import Client
from manages.models import PTRequest
from summits.models import Summit

class PT(models.Model):
    pt = models.OneToOneField(PTRequest, on_delete=models.CASCADE, related_name='pt')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pt')
    summit = models.ForeignKey(Summit, on_delete=models.CASCADE, related_name='pt', null=True, blank=True)
    service_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    thumbnail = models.ImageField(upload_to='')
    link = models.TextField()
    total_link = models.TextField()
    summary = models.TextField()
    summary_business_plan  = models.FileField(upload_to='')
    business_plan = models.FileField(upload_to='')
    pitch_deck = models.FileField(upload_to='')
    traction_data = models.FileField(upload_to='')
    business_type = models.CharField(
        max_length=20,
        choices=BusinessTypeChoices.choices,
    )
    business_progress= models.CharField(
        max_length=20,
        choices=BusinessProgressChoices.choices,
    )
    is_summit = models.BooleanField(default=False)
    is_approve = models.BooleanField(default=False)
    