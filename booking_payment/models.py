
from django.db import models
from rest_framework.exceptions import ValidationError,NotFound,PermissionDenied
from hotel_room_bed.models import Hostel,Hostel_bed
from django.contrib.auth import get_user_model
User = get_user_model()


#  start implement of models





# ================== Booking viewset ===========================
BOOKING_STATUS=(
  ('pending','pending'),
  ('confirmed','confirmed'),
  ('cancelled','cancelled')
)

class Booking(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings",related_query_name="booking")
  hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,related_name="bookings",related_query_name="booking")
  bed=models.ForeignKey(Hostel_bed,on_delete=models.CASCADE,related_name="bookings",related_query_name="booking")
  status=models.CharField(max_length=255,choices=BOOKING_STATUS,default="pending")
  payment_status=models.CharField(max_length=255,choices=BOOKING_STATUS,default="pending")
  payment_date=models.DateTimeField(blank=True,null=True) 
  created_at=models.DateTimeField(auto_now_add=True)

  @property
  def is_paid(self):
    if self.payment_status=="confirmed":
      return True
    return False

  def clean(self):
    if self.bed.is_booked:
      raise ValidationError("Bed is already booked try another bed")

  def save(self, *args, **kwargs):
    self.clean()
    super().save(*args, **kwargs)

  def __str__(self):
    return f"bed booking for bed no {self.bed.bed_no} in {self.hostel.name} by {self.user.profile.name or self.user.username}"
