from rest_framework import serializers
from .models import *

class PTSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    business_type_display = serializers.SerializerMethodField()

    class Meta:
        model = PT
        fields = [
            "id", "thumbnail", "image", "title", "company","service_name",
            "business_type", "business_type_display", "created_at"
        ]

    def get_image(self, obj):
        if obj.client and obj.client.image:
            return obj.client.image.url
        return None

    def get_company(self, obj):
        if obj.client and obj.client.company:
            return obj.client.company
        return None

    def get_business_type_display(self, obj):
        return obj.get_business_type_display()