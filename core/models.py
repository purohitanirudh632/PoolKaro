from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True , null=False)
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

class Ride(models.Model):
    driver = models.ForeignKey(User,on_delete=models.CASCADE , related_name= 'rides')
    source = models.CharField(max_length=1000)
    date = models.DateTimeField()
    destination = models.CharField(max_length=1000)
    seats_count = models.IntegerField()
    # price = models.IntegerField()
    def __str__(self):
        return f"{self.source} to {self.destination} by  {self.driver} on {self.date.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE )
    ride = models.ForeignKey(Ride , on_delete=models.CASCADE,related_name= 'bookings')
    seats_book = models.IntegerField()
    class Meta:
        unique_together = ('user' ,'ride')
    def __str__(self):
        return  f"{self.user.email} booked {self.seats_book} seats  for {self.ride}"    

