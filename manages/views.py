from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from manages.models import PTRequest
from .models import *
from .serializers import *
from users.permissions import IsApprovedUser, IsEntrepreneur, IsInvestor

class VerificationPagination(PageNumberPagination):
    page_size = 20  # 기본 페이지 크기
    page_size_query_param = 'page_size'  # 페이지 크기 변경 가능
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            "category": self.request.query_params.get("category"),
            "page": self.page.number,
            "page_size": self.page.paginator.per_page,
            "total_pages": self.page.paginator.num_pages,
            "total_items": self.page.paginator.count,
            "projects": data
        })

class VerificationAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = VerificationPagination

    def get_queryset(self):
        category = self.request.query_params.get("category", None)

        category_mapping = {
            "회원 승인 요청": ClientRequest.objects.all(),
            "프레젠테이션 승인 요청": PTRequest.objects.all(),
            # "써밋 승인 요청": SummitRequest.objects.all(),
        }

        return category_mapping.get(category, ClientRequest.objects.none())
    
    def get_serializer_class(self):
        category = self.request.query_params.get("category", None)

        serializer_mapping = {
            "회원 승인 요청": ClientVerificationRequestSerializer,
            "프레젠테이션 승인 요청": PTVerificationRequestSerializer,
        }

        return serializer_mapping.get(category, ClientVerificationRequestSerializer)    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        category = request.query_params.get("category")

        if queryset is None or not queryset.exists():
            return Response({"message": "해당 카테고리에 대한 요청이 없습니다.", "requests": []}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response({
            "category": category,
            "requests": serializer.data
        })
    
class UserVerificationDetailAPIView(APIView):
    pass