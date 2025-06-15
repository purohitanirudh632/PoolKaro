from django.urls import path
from .views import RegisterAPIview , RideAPIview ,BookingApiView
from rest_framework_simplejwt.views import (TokenObtainPairView , TokenRefreshView)
urlpatterns = [
    path('register/',RegisterAPIview.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh' ),
    path('create/',RideAPIview.as_view(),name = 'create ride'),
    path('book/',BookingApiView.as_view(),name = 'book ride')
]