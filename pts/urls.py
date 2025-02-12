from django.urls import path

from .views import *

app_name = 'pts'

urlpatterns = [
    path('investors/main/', InvestorMainAPIView.as_view()),
]