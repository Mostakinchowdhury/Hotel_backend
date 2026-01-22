from xml.dom import NotFoundErr
from unicodedata import name
from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model() 

from rest_framework.exceptions import PermissionDenied
# Create your models here.



# =================== hotel model  =============

HOSTEL_TYPE=(
    ("Boys","BOYS"),
    ("Girls","GIRLS")
)
class Hostel(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    benefits=models.TextField()
    is_verified=models.BooleanField(default=False)
    monitor=models.ForeignKey(User,on_delete=models.CASCADE,related_name="hostels",related_query_name="hostel")
    created_at=models.DateTimeField(auto_now_add=True)
    hostel_type=models.CharField(max_length=50,choices=HOSTEL_TYPE)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} -> Monitor : {self.monitor.profile.name or self.monitor.username}"



# =================== hotel room model  =============

class HostelRoom(models.Model):
    hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,related_name="rooms",related_query_name="room")
    room_no=models.CharField(max_length=100)
    bed_capacity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.hostel.name} -> {self.room_no} -> {self.bed_capacity}"
    
    




  # =================== hotel room's bed model  =============


class Hostel_bed(models.Model):
    bed_no=models.CharField(max_length=100)
    room=models.ForeignKey(HostelRoom,on_delete=models.CASCADE,related_name="beds",related_query_name="bed")
    is_booked=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.room.hostel.name} -> {self.room.room_no} -> {self.bed_no} -> {self.is_booked}"



#  ============================= hostel images or video model ===================


class Hostel_images(models.Model):
    file=models.FileField(upload_to="hostel_files")
    hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,related_name="files",related_query_name="file")
    created_at=models.DateTimeField(auto_now_add=True)

    # check file is image or video
    @property
    def is_image(self):
        return self.file.name.endswith(('.png', '.jpg', '.jpeg', '.gif'))
    
    @property
    def is_video(self):
        return self.file.name.endswith(('.mp4', '.avi', '.mkv', '.mov'))

    # ======= highest one hostel can have only 10 images or video
    @classmethod
    def check_limit(cls,hostel):
        if cls.objects.filter(hostel=hostel).count() >= 10:
            return False
        return True

    @classmethod
    def howmuchtocross(cls,hostel):
        if not Hostel.objects.filter(id=hostel).exists():
            raise NotFoundErr("Hostel not found")
        hav= Hostel_images.objects.filter(hostel=hostel).count()

        return f"You can upload {10 - {hav or 0}} files for your hostel"

    # ======= blocked to save if limit cross =========


    def have_limit(self):
        if self.check_limit(self.hostel):
            return True
        return False



    # =================    blocked if not have limit ============


    def save(self, *args, **kwargs):
        if self.have_limit():
            super().save(*args, **kwargs)
        else:
            raise PermissionDenied("Hostel can have only 10 images or video You cross your limit")

     
    def __str__(self):
        return f"{self.hostel.name} -> {self.file}"

