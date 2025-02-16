from .models import *
from rest_framework import serializers

class ClientRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRequest
        exclude = ['manager', 'summit_count', 'pt_count', 'is_approve']

class ClientVerificationRequestSerializer(serializers.ModelSerializer):
    certificate_employment_name = serializers.SerializerMethodField() 

    class Meta:
        model = ClientRequest
        fields = [
            "id", "request_id", "client_position", "name", "phone", "company",
            "certificate_employment_name", "company_email", "requested_at","status",
        ]

    def get_certificate_employment_name(self, obj):
        """ 파일명만 추출하여 반환 """
        if obj.certificate_employment:
            return obj.certificate_employment.name.split("/")[-1]  
        return None
    
class PTVerificationRequestSerializer(serializers.ModelSerializer):
    summary_business_plan_name = serializers.SerializerMethodField() 
    business_plan_name = serializers.SerializerMethodField()
    pitch_deck_name = serializers.SerializerMethodField()
    traction_data_name = serializers.SerializerMethodField()

    class Meta:
        model = PTRequest
        fields = [
            "id","request_id","name","title","link","total_link", "summary_business_plan_name",
            "business_plan_name","pitch_deck_name","traction_data_name","requested_at", "status",
        ]

    def get_summary_business_plan_name(self, obj):
        if obj.summary_business_plan:
            return obj.summary_business_plan.name.split("/")[-1] 
        return None

    def get_business_plan_name(self, obj):
        if obj.business_plan:
            return obj.business_plan.name.split("/")[-1]
        return None

    def get_pitch_deck_name(self, obj):
        if obj.pitch_deck:
            return obj.pitch_deck.name.split("/")[-1]
        return None
    
    def get_traction_data_name(self, obj):
        if obj.traction_data:
            return obj.traction_data.name.split("/")[-1]
        return None
    
class SummitVerificationRequestSerializer(serializers.ModelSerializer):
    pass

class UserVerificationDetailSerializer(serializers.ModelSerializer):
    certificate_employment_name = serializers.SerializerMethodField()

    class Meta:
        model = ClientRequest
        fields = [
            "id", "request_id", "client_position", "name", "phone", "company",
            "certificate_employment", "certificate_employment_name",
            "company_email", "requested_at", "status",
        ]

    def get_certificate_employment_name(self, obj):
        if obj.certificate_employment:
            return obj.certificate_employment.name.split("/")[-1]
        return None