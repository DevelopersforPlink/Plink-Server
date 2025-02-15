from django.db import models
from common.models.choiceModels import BusinessProgressChoices,BusinessTypeChoices
from users.models import Client
from django.apps import apps
from common.utils.fileManger import change_filename

class Summit(models.Model):
    summit_request = models.OneToOneField('manages.SummitRequest', on_delete=models.CASCADE, primary_key=True, related_name='summit')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='summit')
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
    is_approve = models.BooleanField(default=False)

    def get_summit_request_model():
        return apps.get_model('manages', 'SummitRequest')