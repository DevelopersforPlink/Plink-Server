from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('refresh-token/', RefreshAPIView.as_view()),
    path('join/', JoinAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('id-check/', CheckIdAPIView.as_view()),
    path('verification-code/', VerificationCodeAPIView.as_view()),
    path('id/', FindIdAPIView().as_view()),
    path('password/', ResetPwAPIView.as_view()),
]