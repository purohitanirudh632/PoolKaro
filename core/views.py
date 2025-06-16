from django.shortcuts import render
from .serializers import UserSerializer ,RideSerializer ,BookingSerializer
from .models import User , Booking ,Ride
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST , HTTP_200_OK , HTTP_201_CREATED , HTTP_404_NOT_FOUND , HTTP_401_UNAUTHORIZED
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
    def get(self, request):
        ridedata = Ride.objects.all()
        serializer = RideSerializer(ridedata,many =True)
        return Response(serializer.data)

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

    def get(self,request):
        bookings = Booking.objects.filter(user = request.user).all()
        serializer = BookingSerializer(bookings,many =True)
        return Response(serializer.data) 
    
    def post(self,request):
        ride_id = request.data.get('ride_id')
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride does not Exists"} , status= HTTP_404_NOT_FOUND)
        
        total_booked_seats = sum(booking.seats_book for booking in ride.bookings.all())
        seats_left = ride.seats_count  - total_booked_seats
        
        requested_seats = request.data.get('seats_booked',1)

        if requested_seats >seats_left:
            return Response({'detail': f"only {seats_left} seat(s) Left." },status=HTTP_400_BAD_REQUEST)
        
        print(request.user.id , '\n\n\n\n\n')
        booking  = Booking.objects.create(
            ride=ride,
            user = request.user,
            seats_book = requested_seats,
        )

        serializer = BookingSerializer(booking)
        return Response({
            'message': "seats Booked successfully",
            "booking_id" : booking.id,
            "booking": serializer.data
        },status=HTTP_201_CREATED)
        
    def delete(self,request,pk):
        try:
            booking = Booking.objects.get(id=pk)
        except Booking.DoesNotExist():
            return Response({'error': 'booking does not exist'}, status=HTTP_404_NOT_FOUND)
        print(booking.user , request.user)
        if booking.user != request.user:
            return Response({'error':'not the authenticed user'},status=HTTP_401_UNAUTHORIZED)
    
        booking.delete()
        return Response({"message":"your Booking has been cancelled successfully"})

