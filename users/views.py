from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import EmailMessage


from django.contrib.auth import authenticate
# from django.contrib.auth.models import update_last_login

from .models import *
from manages.models import PTRequest
from .serializers import *
from manages.serializers import ClientRequestSerializer, ClientRequestResSerializer

from common.utils.verificationCodeManager import create_code
from common.utils.requestIDGenerator import generate_request_id
from common.models.choiceModels import RequestStatus


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
    
class CheckIdAPIView(APIView):
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
        
        if user := authenticate(username=username, password=password):
            serializer = TokenObtainPairSerializer(data={'username': username, 'password': password})
            # id, 비번 맞나 틀리나 검사
            if serializer.is_valid():
                user.is_code_verificated = True
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

class VerificationCodeAPIView(APIView):
    permission_classes = [AllowAny]

    # 인증코드 발송
    def post(self, request):
        serializer = CodeAuthSerializr(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = create_code()
            if before := CodeForAuth.objects.filter(email=email):
                before.update(is_used=1)
            CodeForAuth.objects.create(email=email, code=code)
            subject = "Plink 이메일 인증 보안코드입니다."
            message = "인증코드는 "+ code + " 입니다."
            to = [email]
            EmailMessage(subject=subject, body=message, to=to).send()
            return Response({"message": "send code success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request): # 인증코드 비교 및 임시토큰 발행
        serializer = CodeAuthSerializr(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data.get("code")
        if email == None or code == None:
            return Response({"message": "no email or code"}, status=status.HTTP_400_BAD_REQUEST)
        if code_obj := CodeForAuth.objects.filter(email=email, is_used=0).first():
            if now() >= code_obj.expiration_time:
                return Response({"message": "Invalid code"})
            code_obj.is_used = 1
            code_obj.save()
            verification_code = code_obj.code
            if code == verification_code:
                if client := Client.objects.filter(company_email=email).first():
                    access = str(RefreshToken.for_user(client.user).access_token)
                    res = Response(
                        {
                            "message": "code is correct",
                            "temporary_access": access
                        },
                        status=status.HTTP_200_OK,
                    )
                    return res 
                res = Response({"message": "code is correct"}, status=status.HTTP_200_OK,)
                return res
            return Response(
                {
                    "message": "코드가 맞지 않습니다. 재전송 후 새로운 코드를 입력해주세요."
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response({"message": "코드를 재전송해주세요."}, status=status.HTTP_400_BAD_REQUEST)

class FindIdAPIView(APIView):
    # 아이디 조회
    def get(self, request):
        user = request.user
        if user:
            return Response({"username": user.username}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Not user"}, status=status.HTTP_404_NOT_FOUND)


class ResetPwAPIView(APIView):
    # pw 변경
    def patch(self, request):
        user = request.user
        password = request.data.get("password", None)
        if password == None:
            return Response({"message": "No password"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message": "password changed."}, status=status.HTTP_202_ACCEPTED)

class ClientInfoAPIView(APIView):
    def get(self, request):
        client = request.user.client
        serializer = ClientResSerializer(client)
        res = serializer.data
        res['status'] = client.client_request.status
        return Response(res, status=status.HTTP_200_OK)
        
    def post(self, request):
        data = request.data.copy()
        user = request.user
        data['user'] = user.id
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            client = serializer.save()
            client.user.is_agree = True
            client.user.save()
            data.pop('user')
            data['client'] = client.user_id
            serializer_request = ClientRequestSerializer(data=data)
            if serializer_request.is_valid():
                serializer_request.save()
                return Response({"message": "등록에 성공했습니다."}, status=status.HTTP_201_CREATED)
            return Response(serializer_request.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        client_request = request.user.client.client_request
        data = request.data
        serializer = ClientRequestSerializer(client_request, data=data, partial=True)
        if serializer.is_valid():
            client_request = serializer.save()
            client_request.request_id = generate_request_id(client_request.get_request_type())
            client_request.is_approve = False
            client_request.status = RequestStatus.PENDING
            client_request.save()
            if client := client_request.client:
                client.is_approve = False
                client.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientUpdateInfoAPIView(APIView):
    def get(self, request):
        client_request = request.user.client.client_request
        serializer = ClientRequestResSerializer(client_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
