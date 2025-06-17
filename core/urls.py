from django.urls import path
from .views import RegisterAPIview , RideAPIview ,BookingApiView ,SearchRide
from rest_framework_simplejwt.views import (TokenObtainPairView , TokenRefreshView)
urlpatterns = [
    path('register/',RegisterAPIview.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh' ),
    path('create/',RideAPIview.as_view(),name = 'create ride'),
    path('get_rides',RideAPIview.as_view(),name = 'get_rides'),
    path('book/',BookingApiView.as_view(),name = 'book ride'),
    path('cancle-booking/<pk>',BookingApiView.as_view(),name = 'deleteBooking'),
    path('search_ride/',SearchRide.as_view(),name ='search Rides')
]