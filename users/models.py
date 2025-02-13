from django.db import models

from common.models.baseModels import BaseModel
from manages.models import ClientRequest
from common.models.choiceModels import ClientPositionChoices
from common.utils.fileManger import change_filename
from common.utils.verificationCodeManager import set_expire

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(username = username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, password=None, **extra_fields):
        superuser = self.create_user(
            username = username,
            password = password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_agree = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

def profile_upload_path(instance, filename):
    return f'profile/{change_filename(filename)}'

def certificate_upload_path(instance, filename):
    return f'certificate-employment/{change_filename(filename)}'

class Client(models.Model):
    client = models.OneToOneField(ClientRequest, on_delete=models.CASCADE, related_name='client_requests')
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
    
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='manager')
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    job = models.CharField(max_length=10)
    hire_date = models.DateField()
    
class Notice(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='notices')
    content = models.TextField()

class CodeForAuth(BaseModel):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    expiration_time = models.DateTimeField(default=set_expire)
