from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import *
from rest_framework.decorators import api_view,permission_classes

from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from hotel_room_bed.mypermissions import *
from .permissions import *




# ============================== Hotel Rating ViewSet ===============================


class HotelRatingViewSet(ModelViewSet):
    queryset = HotelRating.objects.all()
    serializer_class = HotelRatingSerializer
    permission_classes = [IsAuthenticated,IsOwnerorborderoradmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



# ============================= hostel review viewset ===============================



class Hostel_review_viewset(ModelViewSet):
    queryset = Hostel_review.objects.all()
    serializer_class = HostelReviewSerializer
    permission_classes = [IsAuthenticated,IsOwnerorborderoradmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    



# ==================================  Notice ViewSet ===================================


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated,IsMonitororAdmin]



# ================================ Hostel_address viewset ===============



class Hostel_address_viewset(ModelViewSet):
    queryset = Hostel_address.objects.all()
    serializer_class = HostelAddressSerializer
    permission_classes = [IsAuthenticated,IsMonitororAdmin]




# ========================== Hostel_coordinate viewset =====================



class Hostel_coordinate_viewset(ModelViewSet):
    queryset = Hostel_coordinate.objects.all()
    serializer_class = HostelCoordinateSerializer
    permission_classes = [IsAuthenticated,IsMonitororAdmin]



