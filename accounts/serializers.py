from rest_framework import serializers
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .utils import send_otp_via_email

from django.contrib.auth import get_user_model
User=get_user_model()
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    } 

# ===============  profile serializer =================
class ProfileSerializer(serializers.ModelSerializer):
    profile_imag = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'name', 'phone', 'date_of_birth', 'gender',
            'parent_number', 'emergency_contact', 'address', 'bio',
            'profile_image', 'profile_imag'
        ]
        read_only_fields = ['id','profile','created_at','updated_at']

    def get_profile_imag(self,obj):
        request=self.context.get("request",None)
        if request is None:
            return None
        return request.build_absolute_uri(obj.profile_image.url) if obj.profile_image else None


# serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['id', 'email', 'username','password','password2','is_staff','is_superuser',"is_monitor","role","created_at","updated_at","profile"]
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }
    def validate_password(self, value):
        if not value.strip():
            raise serializers.ValidationError("This field cannot be blank.")
        if len(value)<8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value.strip()
    def validate_password2(self, value):
        return value.strip()
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        send_otp_via_email(user)
        return "We sent an OTP to your email. Please check your inbox and verify your account." 

# serializer for user login
class loginserializer(serializers.Serializer):
  password=serializers.CharField(min_length=8)
  email=serializers.EmailField()
  def validate(self, attrs):
     user=authenticate(email=attrs['email'],password=attrs['password'])
     if user is not None:
       if not user.is_verified:
            send_otp_via_email(user)
            attrs['is_verified']=False
            attrs['message']=f"We sent an OTP to your email ({user.email}). Please check your inbox and verify your account."
            return attrs
       attrs['token']=get_tokens_for_user(user)
       attrs['is_verified']=True
     else:
       raise serializers.ValidationError("Your information not match with any record try again")
     return attrs



# ============ changepassword serializer ===========


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

    def validate(self, attrs):
        user = self.context.get('user')
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("New password and confirm password do not match")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")

        return attrs

    def save(self, **kwargs):
        user = self.context.get('user')
        user.set_password(self.validated_data['new_password'])
        user.save()
        return UserRegistrationSerializer(user).data



# =================== resetpassword or forget password password ============


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from .utils import password_reset_email
class ResetPasswordgenaretSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value
    def save(self, **kwargs):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        # Here you would typically send an email with a reset link or token
        # For simplicity, we'll just return the user object
        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"
        send_mail(
                subject="Reset your password",
                message="Click the link to reset your password",
                html_message=password_reset_email(reset_link),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        return "we have sent you a link to reset your password in your email account"


class setResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            if password != confirm_password:
                raise serializers.ValidationError({'confirm_password':"Password and confirm password do not match"})

            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("The reset link is invalid or has expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError("The reset link is invalid or has expired")
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")




