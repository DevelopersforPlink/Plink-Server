from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate
# from django.contrib.auth.models import update_last_login


class RefreshAPIView(APIView):
    permission_classes = [AllowAny]
    # access token 재발급
    def post(self, request):
        refresh = request.COOKIES.get("refresh")
        if not refresh:
            return Response({"message": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            serializer = TokenRefreshSerializer(data={'refresh': refresh})
            if serializer.is_valid():
                res = Response({"access": serializer.validated_data['access']}, status=status.HTTP_200_OK)
            res.set_cookie("refresh", serializer.validated_data['refresh'], httponly=True, samesite="Lax", secure=True)
            return res
        except TokenError as e:
            return Response({"message": f"Invalid token: {e}"}, status=status.HTTP_401_UNAUTHORIZED)
            


class JoinAPIView(APIView):
    permission_classes = [AllowAny]
    # 회원가입
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_200_OK)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class IdCheckAPIView(APIView):
    permission_classes = [AllowAny]
    # 아이디 중복 체크
    def get(self, request):
        username = request.GET.get('username', '')
        if not username:
            return Response({"message": "ID를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            get_object_or_404(User, username=username)
            return Response({"message": "해당 ID는 사용할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "사용할 수 있는 아이디입니다."}, status=status.HTTP_200_OK)
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    # 로그인
    def post(self, request):
        username=request.data.get("username")
        password=request.data.get("password")
        # 로그인 전 쿠키에 있는 리프레시 토큰 무효화
        try:
            refresh = request.COOKIES.get('refresh')
            if refresh:
                refresh_token = RefreshToken(refresh)
                refresh_token.blacklist()
        except TokenError as e:
            pass
        
        if authenticate(username=username, password=password):
            serializer = TokenObtainPairSerializer(data={'username': username, 'password': password})
            # id, 비번 맞나 틀리나 검사
            if serializer.is_valid():
                res = Response(
                    {
                        "message": "login success",
                        "access": serializer.validated_data['access'],
                        "is_agree": serializer.user.is_agree
                    },
                    status=status.HTTP_200_OK,
                )
                res.set_cookie("refresh", serializer.validated_data['refresh'], httponly=True, samesite="Lax", secure=True)
                return res
            else:
                return Response(serializer.errors)
        else: # id, 비번 둘 중 하나가 틀렸을 때
            return Response({"message": "아이디 혹은 비밀번호가 맞지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)