from rest_framework import permissions
from rest_framework.permissions import * 
from rest_framework.request import Request

class IsHostelMonitorOrAdminToUpdateDelete(BasePermission):
    """
    Custom permission to allow only hostel monitors and admins to delete a hostel.
    """
    def has_permission(self, request:Request, view):
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            return bool(
                request.user and 
                request.user.is_authenticated and (
                    request.user.is_superuser or 
                    getattr(request.user, 'is_monitor', False)
                )
            )
        return True

    def has_object_permission(self, request:Request, view, obj):
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            return bool(
                request.user and 
                request.user.is_authenticated and (
                    request.user.is_superuser or 
                    (getattr(request.user, 'is_monitor', False) and obj.monitor == request.user)
                )
            )
        return True



#   ======================   permission class for hostel room and bed and file =============================



class IsMonitorOrAdminorStaff(BasePermission):
    def has_permission(self, request:Request, view):
        # admin can do everything
        if request.user.is_superuser:
            return True
        # staff can do everything except delete
        if request.method not in ["DELETE","PATCH"] and request.user.is_staff:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_monitor', False)
        )

    def has_object_permission(self, request:Request, view, obj):
        if request.user.is_superuser:
            return True
        # staff can do everything except delete
        if request.method not in ["DELETE","PATCH"] and request.user.is_staff:
            return True

        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'is_monitor', False) and request.user == obj.hostel.monitor
        )
