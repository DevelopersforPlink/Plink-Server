from django.db import models
from common.models import BaseModel
from utils.fileManger import change_filename

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

class ClientPositionChoices(models.TextChoices):
    INVESTOR = 'INV', '투자자'
    ENTREPRENEUR = 'ENT', '창업자'

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='client')
    image = models.ImageField(upload_to=profile_upload_path, blank=True)
    company = models.CharField(max_length=50)
    company_position = models.CharField(max_length=10)
    company_email = models.EmailField(max_length=50)
    certificate_employment = models.FileField(upload_to=certificate_upload_path, blank=True)
    is_in_company = models.BooleanField(default=False)
    user_position = models.CharField(choices=ClientPositionChoices.choices, max_length=3)
    is_agree = models.BooleanField(default=False)
    summit_count = models.IntegerField(default=0)
    pt_count = models.IntegerField(default=0)
    verification_code = models.CharField(max_length=6, blank=True)

    @property
    def name(self):
        return self.user.name

    @property
    def phone(self):
        return self.user.phone

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='manager')
    job = models.CharField(max_length=10)
    hire_date = models.DateField()

    @property
    def name(self):
        return self.user.name

    @property
    def phone(self):
        return self.user.phone