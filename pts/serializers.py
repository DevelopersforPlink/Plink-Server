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

class PTCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTRequest
        fields = [
            "thumbnail", "service_name", "title",
            "link", "total_link", "business_type", "summary",
            "summary_business_plan", "business_plan", "pitch_deck",
            "traction_data", "business_progress", "is_summit", "is_approve"
        ]

class PTDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    business_type_display = serializers.SerializerMethodField()

    class Meta:
        model = PT
        fields = [
            "id", "thumbnail", "image", "title", "link", "summary",
            "summary_business_plan", "company", "service_name", "business_type",
            "business_type_display"
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
    
class PostedPTSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    
    class Meta:
        model = PT
        fields = [
            "id", "thumbnail", "title", "company", "service_name", "created_at"
        ]

    def get_company(self, obj):
        if obj.client and obj.client.company:
            return obj.client.company
        return None