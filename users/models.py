from django.db import models
from common.models import BaseModel
from django.conf import settings
from utils.fileManger import change_filename

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        user = self.model(
            username = username,
            password = password,
        )
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

class UserPositionChoices(models.TextChoices):
    INVESTOR = 'INV', '투자자'
    ENTREPRENEUR = 'ENT', '창업자'

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to=f'profile/{change_filename}', blank=True)
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)
    company = models.CharField(max_length=50)
    company_position = models.CharField(max_length=10)
    company_email = models.EmailField(max_length=50)
    certificate_employment = models.FileField(upload_to=f'certificate-employment/{change_filename}', blank=True)
    is_in_company = models.BooleanField(default=False)
    user_position = models.CharField(choices=UserPositionChoices.choices, max_length=3)
    is_agree = models.BooleanField(default=False)
    summit_count = models.IntegerField(default=0)
    pt_count = models.IntegerField(default=0)
    verification_code = models.CharField(max_length=6, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Notice(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()