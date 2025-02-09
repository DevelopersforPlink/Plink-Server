from django.db import models
from common.models import BaseModel, BusinessTypeChoices, BusinessProgressChoices
from users.models import Manager
from utils.fileManger import change_filename

class Summit(BaseModel):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='summits')
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
        default = BusinessTypeChoices.SERVICE
    )
    business_progress = models.CharField(
        max_length=20,
        choices = BusinessProgressChoices.choices,
        default = BusinessProgressChoices.IDEA
    )
    min_video_length = models.DurationField()
    max_video_length = models.DurationField()
    other_requirements = models.TextField()
    participant_count = models.PositiveIntegerField()
