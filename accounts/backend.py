from requests import Request
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
User=get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        if email is None:
            email = username

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import BlacklistedAccessToken

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request:Request):
        result = super().authenticate(request)

        if result is None:
            return None

        user, token = result

        raw_token = token["jti"]
        if BlacklistedAccessToken.objects.filter(token=raw_token).exists():
            raise AuthenticationFailed("Token in blacklist or logged out")

        return user, token
