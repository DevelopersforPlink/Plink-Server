from django.db import models
from common.models.baseModels import BaseRequest
from users.models import Client, Manager
from pts.models import PT
from summits.models import Summit

class PTRequest(BaseRequest):
    pt = models.ForeignKey(PT, on_delete=models.CASCADE, related_name='pt_requests')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='pt_requests')

class SummitRequest(BaseRequest):
    summit = models.ForeignKey(Summit, on_delete=models.CASCADE, related_name='summit_requests')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='summit_requests')

class ClientRequest(BaseRequest):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_requests')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='client_requests')