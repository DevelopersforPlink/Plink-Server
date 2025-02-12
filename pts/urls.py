from django.urls import path

from .views import *

app_name = 'pts'

urlpatterns = [

    path('presentations/', PTCreateAPIView.as_view()),
    path('presentations/<str:pk>/', PTAPIView.as_view()),
]