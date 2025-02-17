from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from manages.models import PTRequest
from .models import *
from pts.models import PT
from common.models.choiceModels import RequestStatus
from .serializers import *
from users.permissions import IsApprovedUser, IsEntrepreneur, IsInvestor
from django.db.models import Case, When, Value, IntegerField

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
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = VerificationPagination

    def get_queryset(self):
        category = self.request.query_params.get("category", None)

        category_mapping = {
            "회원 승인 요청": ClientRequest.objects.annotate(
                priority=Case(
                    When(status=RequestStatus.PENDING, then=Value(1)),  # PENDING이면 우선순위 1
                    default=Value(2),  # 그 외는 2
                    output_field=IntegerField(),
                )
            ).order_by("priority", "-updated_at"),

            "프레젠테이션 승인 요청": PTRequest.objects.annotate(
                priority=Case(
                    When(status=RequestStatus.PENDING, then=Value(1)),  # PENDING이면 우선순위 1
                    default=Value(2),  # 그 외는 2
                    output_field=IntegerField(),
                )
            ).order_by("priority", "-updated_at"),

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
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        client_request = get_object_or_404(ClientRequest, id=pk)

        serializer = UserVerificationDetailSerializer(client_request)

        return Response({
            "message": "회원 검증 요청 상세 페이지 조회 성공",
            "request": serializer.data
        }, status=status.HTTP_200_OK)
                
    def post(self, request, pk):
        client_request = get_object_or_404(ClientRequest, id=pk)
        client = client_request.client

        new_status = request.data.get("status")
        reject_reason = request.data.get("reject_reason")
        manager_id = request.data.get("manager")

        manager = get_object_or_404(Manager, id=manager_id)
        
        if new_status not in [RequestStatus.APPROVED, RequestStatus.REJECTED]:
            return Response({"message": "유효하지 않은 status 값입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status == RequestStatus.REJECTED and not reject_reason:
            return Response({"message": "반려 사유(reject_reason)를 작성해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        client_request.status = new_status
        client_request.is_approve = (new_status == RequestStatus.APPROVED)
        client_request.manager = manager

        if new_status == RequestStatus.REJECTED:
            client_request.reject_reason = reject_reason
        
        client_request.save()

        if new_status == RequestStatus.APPROVED:
            client.name = client_request.name
            client.phone = client_request.phone
            client.image = client_request.image
            client.company = client_request.company
            client.company_position = client_request.company_position
            client.company_email = client_request.company_email
            client.certificate_employment = client_request.certificate_employment
            client.client_position = client_request.client_position
            client.summit_count = client_request.summit_count
            client.pt_count = client_request.pt_count
            client.is_approve = True
            client.save()
            message = "회원 검증 요청 승인 처리 완료"
        else:
            client.is_approve = False
            client.save()
            message = "회원 검증 요청 반려 처리 완료"

        return Response({
            "message": message,
            "request_id": client_request.request_id,
            "reject_reason": client_request.reject_reason,
            "status": client_request.status,
            "is_approve": client_request.is_approve,
            "manager": manager.name
        }, status=status.HTTP_200_OK)
    
class PTVerificationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        presentation_request = get_object_or_404(PTRequest, id=pk)
        serializer = PTVerificationDetailSerializer(presentation_request, context={"request": request})

        return Response({
            "message": "프레젠테이션 요청 상세페이지 조회 성공",
            "request": serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        pt_request = get_object_or_404(PTRequest, id=pk)
        pt = PT.objects.filter(pt_request=pt_request).first()

        new_status = request.data.get("status")
        reject_reason = request.data.get("reject_reason")
        manager_id = request.data.get("manager")

        manager = get_object_or_404(Manager, user_id=manager_id)

        if new_status not in [RequestStatus.APPROVED, RequestStatus.REJECTED]:
            return Response({"message": "유효하지 않은 status 값입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status == RequestStatus.REJECTED and not reject_reason:
            return Response({"message": "반려 사유(reject_reason)를 작성해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        pt_request.status = new_status
        pt_request.is_approve = (new_status == RequestStatus.APPROVED)
        pt_request.manager = manager

        if new_status == RequestStatus.REJECTED:
            pt_request.reject_reason = reject_reason

        pt_request.save()

        if new_status == RequestStatus.APPROVED:
            if pt:
                pt.is_approve = True
                pt.status = RequestStatus.APPROVED
                pt.save()
            else:
                PT.objects.create(
                    pt_request=pt_request,
                    client=pt_request.client,
                    summit=pt_request.summit,
                    service_name=pt_request.service_name,
                    title=pt_request.title,
                    thumbnail=pt_request.thumbnail,
                    link=pt_request.link,
                    total_link=pt_request.total_link,
                    summary=pt_request.summary,
                    summary_business_plan=pt_request.summary_business_plan,
                    business_plan=pt_request.business_plan,
                    pitch_deck=pt_request.pitch_deck,
                    traction_data=pt_request.traction_data,
                    business_type=pt_request.business_type,
                    business_progress=pt_request.business_progress,
                    is_summit=pt_request.is_summit,
                    is_approve=True,
                    status = RequestStatus.APPROVED,
                    created_at = pt_request.created_at
                )
            message = "프레젠테이션 승인 처리 완료"
        else:
            if pt:  # 반려된 경우 PT 테이블도 is_approve=False 처리
                pt.is_approve = False
                pt.status = RequestStatus.REJECTED
                pt.save()
            message = "프레젠테이션 반려 처리 완료"

        return Response({
            "message": message,
            "request_id": pt_request.request_id,
            "reject_reason": pt_request.reject_reason,
            "status": pt_request.status,
            "is_approve": pt_request.is_approve,
            "manager": manager.name
        }, status=status.HTTP_200_OK)