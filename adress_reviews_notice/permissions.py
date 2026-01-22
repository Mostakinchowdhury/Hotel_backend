from hotel_room_bed.models import Hostel
from rest_framework.permissions import BasePermission,SAFE_METHODS
from rest_framework.request import Request
class IsOwnerorborderoradmin(BasePermission):
    def has_permission(self, request:Request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user and request.method in SAFE_METHODS:
            return True

        """ ========================================
         in here check if user alredy customer of this hostel that able to create a review or rating or review other wise not able to create review or rating or review
        ======================================== """

        return False
    def has_object_permission(self, request:Request, view, obj): 
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated and request.user and request.method in SAFE_METHODS:
            return True
        return request.user == obj.user




# ================== ismonitororadminorstaff =======================



class IsMonitororAdmin(BasePermission):
    """
    if user is an admin or staff he can do everything other wise only monitor can create an object and the monitor who are monitor of this perticuler hostel he can only update or delete any existing object
    
    """
    def has_permission(self,request:Request,view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.user.is_authenticated and request.user and request.method in SAFE_METHODS:
            return True
        return request.user.is_monitor

    def has_object_permission(self,request:Request,view,obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.user.is_authenticated and request.user and request.method in SAFE_METHODS:
            return True
        hotel=Hostel.objects.filter(obj.hostel)
        return request.user.is_monitor and hotel.exist() and hotel.first().user==request.user 
        