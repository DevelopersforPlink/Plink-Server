from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, NotFound
from common.models.choiceModels import ClientPositionChoices
from manages.models import PTRequest
from .models import *
from .serializers import *



























































class PTCreateAPIView(APIView):
    # 프레젠테이션 등록
    permission_classes = [IsAuthenticated]
    serializer_class = PTCreateSerializer

    def post(self, request):
        user = self.request.user

        try:
            client = user.clients
        except Client.DoesNotExist:
            return Response({
                "error": "권한이 없습니다.",
                "message": "프레젠테이션을 등록하려면 먼저 투자자 또는 창업자로 등록해야 합니다."
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PTCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        presentation = serializer.save(client=client)

        # 백오피스 프레젠테이션 등록 요청 송신
        PTRequest.objects.create(pt=presentation)

        return Response({
            "message": "프레젠테이션 등록이 요청되었어요.",
            "presentation": PTCreateSerializer(presentation).data
        }, status=status.HTTP_201_CREATED)
    
class PTAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 프레젠테이션 등록 수정 정보 조회
    def get(self, request, pk):
        presentation = get_object_or_404(PT, pk=pk)
        return Response(PTCreateSerializer(presentation).data, status=status.HTTP_200_OK)
    
    # 프레젠테이션 수정
    def patch(self, request, pk):
        presentation = get_object_or_404(PT, pk=pk)

        if request.user.clients != presentation.client:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "본인의 프레젠테이션만 수정할 수 있습니다."
            })
        
        serializer = PTCreateSerializer(presentation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # 백오피스 프레젠테이션 등록 요청 송신
            PTRequest.objects.create(pt=presentation)

            return Response({
                "message": "프레젠테이션 수정이 요청되었어요.",
                "presentation": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 등록한 프레젠테이션 삭제
    def delete(self, request, pk):
        presentation = get_object_or_404(PT, pk=pk)

        if request.user.clients != presentation.client:
            raise PermissionDenied({
                "error": "권한이 없습니다.",
                "message": "본인의 프레젠테이션만 삭제할 수 있습니다."
            })
        
        presentation.delete()
        return Response({"message": "등록한 프레젠테이션이 삭제되었어요."}, status=status.HTTP_200_OK)