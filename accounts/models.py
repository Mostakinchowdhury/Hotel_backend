from django.template.defaultfilters import default
from cloudinary.utils import unique
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Create your models here.
from django.utils import timezone
from .manager import myUserManager
GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    )


# custom user model
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_monitor=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    USERNAME_FIELD="email"
    EMAIL_FIELD="email"
    REQUIRED_FIELDS=["username"]
    objects=myUserManager()
    @property
    def role(self):
        return "Admin" if self.is_superuser else "Staff" if self.is_staff else "Monitor" if self.is_monitor else "User"
    def __str__(self):
       return f"Username- {self.username} - email {self.email}"



# =====================  profile model ==========================

class Profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile',related_query_name='profile')
    name=models.CharField(max_length=100,default="Not set")
    phone=models.CharField(max_length=20,null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    parent_number=models.CharField(max_length=20,null=True,blank=True)
    emergency_contact=models.CharField(max_length=20,null=True,blank=True)
    address=models.CharField(max_length=100,default='village,thana,district')
    bio=models.TextField(max_length=320,null=True,blank=True)
    profile_image=models.ImageField(upload_to="profile",blank=True,null=True)
    def __str__(self):
        return f"{self.user.username} {self.user.email}'s Profile"


class BlacklistedAccessToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token