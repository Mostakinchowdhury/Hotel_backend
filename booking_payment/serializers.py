from booking_payment.models import BOOKING_STATUS
from rest_framework import serializers
from .models import *


# =====================  write booking serializers class in here  ==============


class Booking_serializer(serializers.ModelSerializer):
  user=serializers.SlugRelatedField(slug_field="username",read_only=True)
  hostel_name=serializers.SlugRelatedField(slug_field="name",read_only=True,source="hostel")
  class Meta:
    model=Booking
    fields=["user","hostel","bed","status","id","created_at","payment_status","payment_date","is_paid","hostel_name"]
    read_only_fields=["user","id","created_at","payment_status","payment_date","status","is_paid","hostel_name"]
  
  def validate_bed(self,bed):
    thisbed=bed if isinstance(bed,Hostel_bed) else Hostel_bed.objects.get(id=bed)
    if thisbed.is_booked:
      raise serializers.ValidationError("Bed is already booked please try another bed")
    return thisbed