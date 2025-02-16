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
            "certificate_employment", "certificate_employment_name", "company_position",
            "company_email", "requested_at",
        ]

    def get_certificate_employment_name(self, obj):
        if obj.certificate_employment:
            return obj.certificate_employment.name.split("/")[-1]
        return None
    
class PTVerificationDetailSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    upload_location = serializers.SerializerMethodField()

    class Meta:
        model = PTRequest
        fields = [
            "id", "request_id", "requested_at", "client_position",
            "name", "phone", "company", "company_position",
            "company_email", "business_type", "business_progress",
            "summary", "upload_location", "link", "total_link", "file",
        ]


    def get_file(self, obj):
        request = self.context.get("request")
        if not request:
            return None

        file_type = request.query_params.get("file", None)

        file_mapping = {
            "one_minute_presentation": obj.link,
            "total_presentation": obj.total_link,
            "summary_business_plan": obj.summary_business_plan.url if obj.summary_business_plan else None,
            "business_plan": obj.business_plan.url if obj.business_plan else None,
            "pitch_deck": obj.pitch_deck.url if obj.pitch_deck else None,
            "traction_data": obj.traction_data.url if obj.traction_data else None,
        }

        if file_type and file_type in file_mapping and file_mapping[file_type]:
            return {file_type : file_mapping[file_type]}
        return None
    
    def get_upload_location(self, obj):
        if obj.is_summit:
            summit_title = obj.summit.title if obj.summit else "써밋 정보 없음"
            return f"써밋: {summit_title}"
        return "전체 프레젠테이션"
