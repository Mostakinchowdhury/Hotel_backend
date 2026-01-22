from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import * 
from .mypermissions import *
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.





# =================== hostel view  ==============


class Hostel_view(ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated,IsHostelMonitorOrAdminToUpdateDelete]
    
    def get_queryset(self):
        return Hostel.objects.all() if (self.request.user.is_superuser or self.request.user.is_staff) else Hostel.objects.filter(monitor=self.request.user) if self.request.user.is_monitor else None

    # ========== pass request.user to serializer save method =========

    def perform_create(self, serializer):
      serializer.save(monitor=self.request.user)

    def perform_update(self, serializer):
      serializer.save(monitor=self.request.user)



# ===========================    hostel room view  =========================== 



class Hostel_room_view(ModelViewSet):
    queryset = HostelRoom.objects.all()
    serializer_class = HostelRoomSerializer
    permission_classes = [IsAuthenticated,IsMonitorOrAdminorStaff]
    
    def get_queryset(self):
        return HostelRoom.objects.all() if (self.request.user.is_superuser or self.request.user.is_staff) else HostelRoom.objects.filter(hostel__monitor=self.request.user) if self.request.user.is_monitor else None


# ===========================    hostel bed view  =========================== 


class Hostel_bed_view(ModelViewSet):
    queryset = Hostel_bed.objects.all()
    serializer_class = HostelBedSerializer
    permission_classes = [IsAuthenticated,IsMonitorOrAdminorStaff]
    
    def get_queryset(self):
        return Hostel_bed.objects.all() if (self.request.user.is_superuser or self.request.user.is_staff) else Hostel_bed.objects.filter(room__hostel__monitor=self.request.user) if self.request.user.is_monitor else None


# ===========================    hostel images view  =========================== 


class Hostel_images_view(ModelViewSet):
    queryset = Hostel_images.objects.all()
    serializer_class = HostelImagesSerializer
    permission_classes = [IsAuthenticated,IsMonitorOrAdminorStaff]
    
    def get_queryset(self):
        return Hostel_images.objects.all() if (self.request.user.is_superuser or self.request.user.is_staff) else Hostel_images.objects.filter(hostel__monitor=self.request.user) if self.request.user.is_monitor else None



# =========== can upload to hostel or not  ===========

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def haslimittoupload(request:Request):
    if not request.data.get("hostel_id"):
         return Response({
            "status":False,
            "message":"Sorry Hostel id missing"
         },status.HTTP_422_UNPROCESSABLE_ENTITY)
    if not Hostel.objects.filter(id=request.data.get("hostel_id")).exists():
        return Response({
            "status":False,
            "message":"Sorry Hostel not found"
        },status.HTTP_404_NOT_FOUND)

    hostel=Hostel.objects.get(id=request.data.get("hostel_id"))
    haslimit=Hostel_images.check_limit(hostel)
    if not haslimit:
        return Response({
            "message":"You already cross your limit"
        },status.HTTP_200_OK)
    return Response({
        "message":Hostel_images.howmuchtocross(hostel)
    })

    if request.user.is_superuser or request.user.is_staff:
        return Response({"can_upload": True})
    return Response({"can_upload": False}) 