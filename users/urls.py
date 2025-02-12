from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('refresh-token/', RefreshAPIView.as_view()),
    path('join/', JoinAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('id-check/', IdCheckAPIView.as_view()),
]