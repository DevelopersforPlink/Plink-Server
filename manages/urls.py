from django.urls import path

from .views import *

app_name = 'manages'

urlpatterns = [
    path('verification-requests/', VerificationAPIView.as_view()),
    path('users/<str:pk>/verification-requests/', UserVerificationDetailAPIView.as_view()),
    path('presentations/<str:pk>/verification-requests/', PTVerificationDetailAPIView.as_view()),
]