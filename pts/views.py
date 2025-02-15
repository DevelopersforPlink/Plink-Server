from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from common.models.choiceModels import ClientPositionChoices, RequestStatus
from manages.models import PTRequest
from .models import *
from .serializers import *
from users.permissions import IsApprovedUser, IsEntrepreneur, IsInvestor

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
            client = user.client
        except Client.DoesNotExist:
            raise PermissionDenied({
                "error": "접근 권한이 없습니다.",
                "message": "투자자만 이 페이지를 볼 수 있습니다."
            })
        
        if client.client_position != ClientPositionChoices.INVESTOR:
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

class PTCreateAPIView(APIView):
    # 프레젠테이션 등록
    permission_classes = [IsAuthenticated]
    serializer_class = PTCreateSerializer

    def post(self, request):
        user = self.request.user

        try:
            client = user.client
        except Client.DoesNotExist:
            return Response({
                "error": "권한이 없습니다.",
                "message": "프레젠테이션을 등록하려면 먼저 투자자 또는 창업자로 등록해야 합니다."
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PTCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        presentation = serializer.save(client=client)

        return Response({
            "message": "프레젠테이션 등록이 요청되었어요.",
            "presentation": PTCreateSerializer(presentation).data
        }, status=status.HTTP_201_CREATED)
    
class PTAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEntrepreneur]

    def post(self, request,pk):
        pt_request = get_object_or_404(PTRequest, pk=pk)

        if request.user.client != pt_request.client:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "본인의 프레젠테이션만 선택할 수 있습니다."
            })
        
        choice = request.data.get("choice")
        if choice not in ["previous", "current"]:
            return Response({
                "error": "잘못된 요청입니다.",
                "message": "choice 값은 'previous' 또는 'current'만 가능합니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if hasattr(pt_request, 'pt') and pt_request.pt:
            presentation = pt_request.pt
            if choice == "previous":
                pt_request.service_name = presentation.service_name
                pt_request.title = presentation.title
                pt_request.thumbnail = presentation.thumbnail
                pt_request.link = presentation.link
                pt_request.total_link = presentation.total_link
                pt_request.summary = presentation.summary
                pt_request.summary_business_plan = presentation.summary_business_plan
                pt_request.business_plan = presentation.business_plan
                pt_request.pitch_deck = presentation.pitch_deck
                pt_request.traction_data = presentation.traction_data
                pt_request.business_type = presentation.business_type
                pt_request.business_progress = presentation.business_progress
                pt_request.is_approve = False
                pt_request.save()
                return Response({
                    "message": "이전 프레젠테이션 버전이 선택되었습니다.",
                    "presentation": {
                        "id": pt_request.id,
                        "title": pt_request.title,
                        "is_approve": pt_request.is_approve
                    }
                }, status=status.HTTP_200_OK)
        return Response({
            "message": "수정된 프레젠테이션이 유지되었습니다.",
            "presentation": {
                "id": pt_request.id,
                "title": pt_request.title,
                "is_approve": False
            }
        }, status=status.HTTP_200_OK)    

    # 프레젠테이션 등록 수정 정보 조회
    def get(self, request, pk):
        presentation = get_object_or_404(PTRequest, pk=pk)
        return Response(PTCreateSerializer(presentation).data, status=status.HTTP_200_OK)
    
    # 프레젠테이션 수정
    def patch(self, request, pk):
        presentation = get_object_or_404(PTRequest, pk=pk)

        if request.user.client != presentation.client:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "본인의 프레젠테이션만 수정할 수 있습니다."
            })
        
        serializer = PTCreateSerializer(presentation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "프레젠테이션 수정이 요청되었어요.",
                "presentation": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 등록한 프레젠테이션 삭제
    def delete(self, request, pk):
        client = request.user.client
        presentation = PT.objects.filter(pk=pk, client=client).first()
        pt_request = PTRequest.objects.filter(pt=presentation).first()

        if presentation and presentation.client != client:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "본인의 프레젠테이션만 삭제할 수 있습니다."
            })
        if presentation and pt_request:
            pt_request.delete()
            presentation.delete()
            return Response({"message": "등록한 프레젠테이션이 삭제되었어요."}, status=status.HTTP_200_OK)
        if pt_request:
            status_message = ""
            if pt_request.status == RequestStatus.PENDING:
                status_message = "승인 대기 중이던 프레젠테이션이 삭제되었어요."
            elif pt_request.status == RequestStatus.REJECTED:
                status_message = "반려된 프레젠테이션이 삭제되었어요."

            pt_request.delete()
            return Response({
                "message": status_message
            }, status=status.HTTP_200_OK)
        
class PTDetailAPIView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self, request, pk):
        presentation = get_object_or_404(PT, pk=pk)
        serializer = PTDetailSerializer(presentation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostedPTPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "page": self.page.number,
            "page_size": self.page.paginator.per_page,
            "total_pages": self.page.paginator.num_pages,
            "total_items": self.page.paginator.count,
            "presentations": data
        })

class PostedPTListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostedPTSerializer
    pagination_class = PostedPTPagination

    def get_queryset(self):
        user = self.request.user

        try:
            client = user.client
        except Client.DoesNotExist:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "창업가로 등록된 사용자만 접근할 수 있습니다."
            })
        
        if client.user_position != ClientPositionChoices.ENTREPRENEUR:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "이 페이지는 창업가 전용입니다."
            })

        return PT.objects.filter(client=client).order_by('-created_at')


