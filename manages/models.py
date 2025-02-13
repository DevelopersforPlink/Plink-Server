from django.db import models
from common.models.baseModels import BaseRequest
from common.models.choiceModels import ClientPositionChoices
from users.models import Client, Manager, User
from common.utils.fileManger import change_filename
from common.models.choiceModels import BusinessProgressChoices, BusinessTypeChoices
from summits.models import Summit

class PTRequest(BaseRequest):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='pt_requests', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='pts')
    summit = models.ForeignKey(Summit, on_delete=models.CASCADE, related_name='pts', null=True, blank=True)
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

class SummitRequest(BaseRequest):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='summit_requests', null=True, blank=True)
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
    is_approve = models.BooleanField(default=False)

def profile_upload_path(instance, filename):
    return f'profile/{change_filename(filename)}'

def certificate_upload_path(instance, filename):
    return f'certificate-employment/{change_filename(filename)}'


class ClientRequest(BaseRequest):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='client_requests', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='client')
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to=profile_upload_path, blank=True)
    company = models.CharField(max_length=50)
    company_position = models.CharField(max_length=10)
    company_email = models.EmailField(max_length=50)
    certificate_employment = models.FileField(upload_to=certificate_upload_path, blank=True)
    is_in_company = models.BooleanField(default=False)
    client_position = models.CharField(choices=ClientPositionChoices.choices, max_length=3)
    summit_count = models.IntegerField(default=0)
    pt_count = models.IntegerField(default=0)
    is_approve = models.BooleanField(default=False)    