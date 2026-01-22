from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import include
router=DefaultRouter()

router.register("hostel",Hostel_view,"hostel")
router.register("hostel_room",Hostel_room_view,"hostel_room")
router.register("hostel_bed",Hostel_bed_view,"hostel_bed")
router.register("hostel_images",Hostel_images_view,"hostel_images")

urlpatterns = [
    path("",include(router.urls)),
    path("haspermissiontoupload/",haslimittoupload)
]
