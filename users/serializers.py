from .models import User
from rest_framework import serializers

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CodeAuthSerializr(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

