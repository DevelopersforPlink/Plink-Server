from rest_framework import serializers
from .models import *


























class PTCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PT
        fields = [
            "thumbnail", "service_name", "title",
            "link", "total_link", "business_type", "summary",
            "summary_business_plan", "business_plan", "pitch_deck",
            "traction_data", "business_progress", "is_summit"
        ]