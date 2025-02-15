from rest_framework import serializers
from .models import *

class PTSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pt_request.id", read_only=True)
    profile = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = PT
        fields = [
            "id", "thumbnail", "profile", "title", "company","service_name",
            "business_type", "business_progress", "is_approve", "created_at"
        ]

    def get_profile(self, obj):
        if obj.client and obj.client.image:
            return obj.client.image.url
        return None

    def get_company(self, obj):
        if obj.client and obj.client.company:
            return obj.client.company
        return None

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
    id = serializers.CharField(source="pt_request.id", read_only=True)
    profile = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = PT
        fields = [
            "id", "thumbnail", "profile", "title", "link", "summary","is_approve",
            "summary_business_plan", "company", "service_name", "business_type"
            ]

    def get_profile(self, obj):
        if obj.client and obj.client.image:
            return obj.client.image.url
        return None

    def get_company(self, obj):
        if obj.client and obj.client.company:
            return obj.client.company
        return None
    
class PostedPTSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pt_request.id", read_only=True)
    company = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    
    class Meta:
        model = PT
        fields = [
            "id", "thumbnail", "title", "type", "company", "service_name", "is_approve", "created_at"
        ]

    def get_company(self, obj):
        if isinstance(obj, PTRequest):
            return obj.client.company if obj.client and obj.client.company else None
        return obj.client.company if obj.client and obj.client.company else None
    
    def get_type(self, obj):
        if isinstance(obj, PTRequest):
            pt = getattr(obj, "pt", None)  # PT가 존재하는지 확인
            if not pt and not obj.is_approve:
                return "심사중"  # PT가 없고 PTRequest의 is_approve=False
            elif pt and not pt.is_approve and not obj.is_approve:
                return "수정중"
            return None # 기본값: 승인된 경우
        
    def get_pt_request_id(self, obj):
        if isinstance(obj, PTRequest):
            return obj.id
        return getattr(obj, "pt_request", None) and obj.pt_request.id