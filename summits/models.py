from django.db import models
from common.models import BaseModel
from utils.fileManger import change_filename


class PT(BaseModel):
    service_name = models.TextField()
    title = models.TextField()
    thumbnail = models.ImageField(upload_to='')
    link = models.TextField()
    total_link = models.TextField()
    business_type = models.CharField(max_length=50)
    summary = models.TextField()
    summary_business_plan = models.FileField(upload_to='')
    business_plan = models.FileField(upload_to='')
    pitch_deck = models.FileField(upload_to='')
    traction_data = models.FileField(upload_to='')
    business_progress = models.CharField(max_length=20)
    is_summit = models.BooleanField(default=False)
    
