from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import *
from django.contrib.auth import get_user_model

User=get_user_model()


# ========================= Booking viewset =========================


class BookingViewSet(ModelViewSet):
  queryset=Booking.objects.all()
  serializer_class=Booking_serializer
  permission_classes=[IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  def perform_update(self, serializer):
    serializer.save(user=self.request.user)

  def perform_destroy(self, instance):
    if not (self.request.is_staff or self.request.user.is_superuser):
      raise PermissionDenied("You are not allowed to delete this booking")
    instance.delete()

  def get_queryset(self):
    return Booking.objects.all() if (self.request.user.is_staff or self.request.user.is_superuser) else Booking.objects.filter(user=self.request.user)
