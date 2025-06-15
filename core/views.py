from django.shortcuts import render
from .serializers import UserSerializer ,RideSerializer ,BookingSerializer
from .models import User , Booking ,Ride
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST , HTTP_200_OK , HTTP_201_CREATED , HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated , AllowAny
# Create your views here.
class RegisterAPIview(APIView):
    def post(self,request):
        serlializer = UserSerializer(data = request.data)
        if serlializer.is_valid():
            serlializer.save()
            return Response({"message" : "user Registered Successfully"} ,status=HTTP_200_OK)
        else:
            return Response(serlializer.errors, status= HTTP_400_BAD_REQUEST)
    
     
class RideAPIview(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes=[AllowAny]
    def post(self,request):
        serializer = RideSerializer(data = request.data)
        if serializer.is_valid():
            ride = serializer.save(driver = request.user)
            return Response({"ride_id": ride.id,"ride" : serializer.data ,"message" : "Your Ride has been created sucessfully"},status = HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)    
        
    
class BookingApiView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes=[AllowAny]
        
    def post(self,request,ride_id):
        try:
            ride = Ride.objects.get(id = ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride does not Exists"} , status= HTTP_404_NOT_FOUND)
        
        total_booked_seats = sum(booking.seats_book for booking in Ride.bookings.all())
        seats_left = ride.seats_count  - total_booked_seats
        requested_seats = request.data.get('seats_booked',1)

        if requested_seats >seats_left:
            return Response({'detail': f"only {seats_left} seat(s) Left." },status=HTTP_400_BAD_REQUEST)
        
        booking  = Booking.objects.create(
            ride=ride,
            passenger = request.user,
            seats_booked = requested_seats,
        )

        serializer = BookingSerializer(booking)
        return Response({
            'message': "seats Booked successfully",
            "booking_id" : booking.id,
            "booking": serializer.data
        },status=HTTP_201_CREATED)
        

