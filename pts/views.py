from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from common.models.choiceModels import ClientPositionChoices
from .models import *
from .serializers import *

class InvestorMainPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "category": self.request.query_params.get("category", "ALL"),
            "page": self.page.number,
            "page_size": self.page.paginator.per_page,
            "total_pages": self.page.paginator.num_pages,
            "total_items": self.page.paginator.count,
            "projects": data
        })

class InvestorMainAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PTSerializer
    pagination_class = InvestorMainPagination

    def get_queryset(self):
        user = self.request.user

        try:
            client = user.clients
        except Client.DoesNotExist:
            raise PermissionDenied({
                "error": "접근 권한이 없습니다.",
                "message": "투자자만 이 페이지를 볼 수 있습니다."
            })
        
        if client.user_position != ClientPositionChoices.INVESTOR:
            raise PermissionDenied({
                "error": "접근 권한이 없습니다.",
                "message": "투자자만 이 페이지를 볼 수 있습니다."
            })

        category = self.request.query_params.get("category", "ALL")
        page = self.request.query_params.get("page", "1")
        page_size = self.request.query_params.get("page_size", "12")

        if not page.isdigit() or int(page) < 1:
            raise NotFound({
                "error": "잘못된 페이지 번호입니다.",
                "message": "Page must be a positive integer."
            })
            
        
        if not page_size.isdigit() or int(page_size) < 1:
            raise NotFound({
                "error": "잘못된 페이지 크기입니다.",
                "message": "Page size must be a positive integer."
            })
        
        queryset = PT.objects.all().order_by('-created_at')

        valid_categories = [choice[0] for choice in BusinessTypeChoices.choices]

        if category != "ALL":
            if category not in valid_categories:
                raise NotFound({
                    "error": "잘못된 카테고리입니다.",
                    "message": f"Valid categories: {valid_categories}"
                })
            queryset = queryset.filter(business_type=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)