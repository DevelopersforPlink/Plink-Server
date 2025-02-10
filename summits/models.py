from django.db import models
from common.models.baseModels import BaseModel
from common.models.choiceModels import BusinessProgressChoices,BusinessTypeChoices
from users.models import Client
from common.utils.fileManger import change_filename

class Summit(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='summits')
    thumbnail = models.ImageField(upload_to='')
    title = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    host = models.CharField(max_length=30)
    management = models.CharField(max_length=30)
    business_type = models.CharField(
        max_length = 20,
        choices = BusinessTypeChoices.choices,
    )
    business_progress = models.CharField(
        max_length=20,
        choices = BusinessProgressChoices.choices,
    )
    min_video_length = models.DurationField()
    max_video_length = models.DurationField()
    other_requirements = models.TextField(blank=True)
    participant_count = models.PositiveIntegerField(default=0)
