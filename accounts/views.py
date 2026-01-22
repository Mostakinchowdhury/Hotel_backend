
from accounts.serializers import UserRegistrationSerializer
from PIL.ImageShow import register
from rest_framework.decorators import api_view,permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated

from rest_framework import status
from django.contrib.auth import get_user_model 
User = get_user_model()
from datetime import datetime
# Create your views here.

# =============== wellcome view ===========

@api_view()
@permission_classes([AllowAny])
def wellcome(request:Request):
  print(f"wellcome ✅ {datetime.now()}")
  data=request.query_params.dict()
  return Response({"message":"Welcome to the API",
  "data":data,
  "user":User.objects.first().password},200)



# =============== login view ===========

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request:Request):
  serializer = loginserializer(data=request.data)
  serializer.is_valid(raise_exception=True)

  if not serializer.validated_data.get("is_verified")==True: 
    return Response({"message":serializer.validated_data.get("message"), 
    "is_verified":serializer.validated_data.get("is_verified")}, 
     status=status.HTTP_400_BAD_REQUEST)
      
  return Response({"message":"Congratulation you are succesfully loged in",
  "is_verified":serializer.validated_data.get("is_verified"),
  **serializer.validated_data['token']}, status=status.HTTP_200_OK)


# ==================== register view ==========
class register_view(APIView):
    permission_classes = [AllowAny]
    def post(self, request:Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            res=serializer.save()
            return Response({
              "status":True,
              "message":res
            },status=status.HTTP_201_CREATED)

        key,value=next(iter(serializer.errors.items()))
        return Response({
          "message":f"{key} -> {value[0]}",
          "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    # login users serialize data
    def get(self, request:Request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserRegistrationSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==================== logout view ===========


from .models import BlacklistedAccessToken
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request:Request):
    if not request.data.get("refresh"):
        return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
    try: 
            # refresh token blacklist

            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            if not token:
                return Response({"detail": "Invalid Refresh Token"}, status=status.HTTP_400_BAD_REQUEST)
            token.blacklist()


            # access token blacklist
            if not request.auth:
                return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
            access=request.auth if isinstance(request.auth, AccessToken) else AccessToken(request.auth) 
            if not access or not isinstance(access, AccessToken):
                return Response({"detail": "Invalid access token"}, status=status.HTTP_400_BAD_REQUEST)
            
            BlacklistedAccessToken.objects.create(
                token=access["jti"],
                user=request.user
            )
            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
    except Exception as e:
            return Response(
                {"detail": "Invalid token",
                "erros":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ) 






# =============  password reset and forget password view ===========


# 🔹 Change Password
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request:Request):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            user=serializer.save()
            return Response({"message": "Password changed successfully",'user':user}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Password Reset (Send Email)
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request:Request):
        serializer = ResetPasswordgenaretSerializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.save()
            return Response({"message": msg}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 🔹 Password Reset (Set New Password)
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request:Request):
        serializer = setResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.utils import timezone
from .utils import *
from threading import Thread

# verify email with otp when user register

class verify_register_otp(APIView):
    permission_classes = [AllowAny]
    def post(self, request:Request):
        otp = request.data.get("otp")
        email = request.data.get("email")
        if not otp:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
         user = User.objects.get(email=email)
         if user.is_verified:
             return Response({"error": "Email is already verified"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
           return Response({"error": "User not found try again"}, status=status.HTTP_404_NOT_FOUND)

        if user.otp_code == otp and user.otp_expiry > timezone.now():
           user.is_verified = True
           user.otp_code = None
           user.save()
           Thread(target=send_welcome_email, args=[user]).start()
           token=get_tokens_for_user(user)
           Profile.objects.get_or_create(user=user)
           return Response({"message": "Email verified successfully",'tokens':token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired OTP. Click the Resend OTP button to try again."}, status=status.HTTP_400_BAD_REQUEST)

    # resend otp if user click the resend otp button by get method
    def get(self, request):
        email = request.GET.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
         user = User.objects.get(email=email)
        except User.DoesNotExist:
           return Response({"error": "User not found try again"}, status=status.HTTP_404_NOT_FOUND)
        if user.is_verified:
            return Response({"message": "Your email is already verified, please log in."}, status=status.HTTP_200_OK)
        send_otp_via_email(user)
        return Response({"message": "A new OTP has been sent to your email. Check it and fill in the OTP input."}, status=status.HTTP_200_OK)



# ========== cheak authentication =====================

from rest_framework.request import Request
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cheak_authentication(request:Request):
    return Response({"message": "You are authenticated",
    "user":UserRegistrationSerializer(request.user).data},
     status=status.HTTP_200_OK) 