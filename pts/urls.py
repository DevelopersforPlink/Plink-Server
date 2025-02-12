from django.urls import path

from .views import *

app_name = 'pts'

urlpatterns = [
    path('investors/main/', InvestorMainAPIView.as_view()),
    path('presentations/', PTCreateAPIView.as_view()),
    path('presentations/uploaded/', PostedPTListAPIView.as_view()),
    path('presentations/<str:pk>/', PTAPIView.as_view()),
    path('presentations/<str:pk>/pages/', PTDetailAPIView.as_view()),
]