from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_active')

@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('user_id',)