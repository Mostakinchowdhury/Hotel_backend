"""
URL configuration for hotel_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include
from django.contrib import admin
from django.urls import path
from accounts import urls as accounts_urls
from hotel_room_bed import urls as hotel_room_bed_urls
from adress_reviews_notice import urls as adress_reviews_notice_urls
from booking_payment import urls as booking_payment_urls

urlpatterns = [
    path("",include(hotel_room_bed_urls)),
    path("",include(adress_reviews_notice_urls)),
    path("",include(booking_payment_urls)),
    path('admin/', admin.site.urls),
    path("auth/",include(accounts_urls)),
] 
