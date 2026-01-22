from adress_reviews_notice.views import Hostel_address_viewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register(r'address',Hostel_address_viewset,"address")

router.register(r'coordinate',Hostel_coordinate_viewset,"coordinate")

router.register(r'reviews', Hostel_review_viewset,"reviews")

router.register(r'notices', NoticeViewSet,"notices")

router.register(r'rating', HotelRatingViewSet,"rating")

urlpatterns = [
    path('', include(router.urls)),
]