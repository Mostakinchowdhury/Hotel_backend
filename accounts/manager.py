from django.contrib.auth.base_user import BaseUserManager
# custom manager for cartitem,cart model include get_create method

# import base manager

from rest_framework.serializers import ValidationError


class myUserManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_field):
        if not username:
            raise ValidationError("Missing import field username")
        if not email:
            raise ValidationError("Email is a requred field")
        email=self.normalize_email(email)
        user=self.model(username=username,email=email,password=password,**extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password=None,**extra_field):
        if not username:
          raise ValidationError("Missing important field username")
        if not email:
          raise ValidationError("Missing important field email")
        if not password:
          raise ValidationError("Missing importnat field password")

        extra_field.setdefault("is_superuser",True)
        extra_field.setdefault("is_staff",True)
        extra_field.setdefault("is_active",True)
        extra_field.setdefault("is_verified",True)
        return self.create_user(username,email,password,**extra_field)
    def create_monitor(self,username,email,password=None,**extra_field):
      if not username:
          raise ValidationError("Missing important field username")
      if not email:
          raise ValidationError("Missing important field email")
      if not password:
          raise ValidationError("Missing importnat field password")
      extra_field.setdefault("is_monitor",True)
      email=self.normalize_email(email)
      user=self.model(username=username,email=email,password=password,**extra_field)
      user.set_password(password)
      user.save(using=self._db)
      return user
    def active_user(self):
        return self.get_queryset().filter(is_active=True)
