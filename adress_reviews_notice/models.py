from _interpchannels import create
from django.db import models
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from hotel_room_bed.models import Hostel
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


# ====================== Hotel Rating Model ====================== 


class HotelRating(models.Model):
   rating = models.PositiveIntegerField()
   user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='hotel_ratings',related_query_name='hotel_rating') 
   hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,related_name='hotel_ratings',related_query_name='hotel_rating')
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f'Rating {self.rating} by {self.user.username} for {self.hostel.name}' 



# ====================== Hotel Review Model ======================  


class Hostel_review(models.Model):
  content=models.TextField()
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='hotel_reviews',related_query_name='hotel_review')
  hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,related_name='hotel_reviews',related_query_name='hotel_review')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Review by {self.user.username} for {self.hostel.name}'  



# ================== Notice ====================


class Notice(models.Model):
  hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,related_name='notices',related_query_name='notice')
  title=models.CharField(max_length=255)
  content=models.TextField()
  is_global=models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Notice {self.title} for {self.hostel.name}'



# ====================== hostel adress ===============


class Hostel_address(models.Model):
  division=models.CharField(max_length=255)
  district=models.CharField(max_length=255)
  thana=models.CharField(max_length=255)
  hostel=models.OneToOneField(Hostel,on_delete=models.CASCADE,related_name='hostel_address',related_query_name='hostel_address')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Address for {self.hostel.name}'


# =======================  Hostel coordinates ======================


class Hostel_coordinate(models.Model):
  hostel=models.OneToOneField(Hostel,on_delete=models.CASCADE,related_name='hostel_coordinate',related_query_name='hostel_coordinate')
  lat=models.CharField(max_length=255)
  lng=models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Coordinates for {self.hostel.name}'  

  
  