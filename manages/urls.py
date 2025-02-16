from django.urls import path

from .views import *

app_name = 'manages'

urlpatterns = [
    path('verification-requests/', VerificationAPIView.as_view()),
    path('users/verification-requests/<str:pk>/', UserVerificationDetailAPIView.as_view()),
]