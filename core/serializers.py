from rest_framework import serializers
from .models import Booking,Ride
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only =True)
    class Meta:
        model = User
        fields = ['first_name','last_name' , 'email' , 'password']

    def create(self, validated_data):
        user = User(
        first_name = validated_data['first_name'],
        last_name = validated_data['last_name'],
        email = validated_data['email']
        )
        user.set_password(validated_data['password'])   # hashes THe Password
        user.save()
        return user
    

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id' , 'driver' ,'source','date','destination','seats_count']
        read_only_fields = ["driver"]
    
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields =  "__all__"
        read_only_fields = ["user"]
