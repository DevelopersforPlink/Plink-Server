from .models import *
from rest_framework import serializers

class ClientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        exclude = ['manager', 'summit_count', 'pt_count', 'is_approve']

class ClientRequestResSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        exclude = ['manager']