
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view.as_view(), name='register'),
    path("wellcome/",wellcome,name="wellcome"),
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),
    path("reset_password_request/",
    PasswordResetRequestView.as_view(),name="reset_password_request"),
    path("reset_password_confirm/",
    PasswordResetConfirmView.as_view(),name="reset_password_confirm"), 
    path("verify_register_otp/",
    verify_register_otp.as_view(),name="verify_register_otp"),
    path("cheak_authentication/",
    cheak_authentication,name="cheak_authentication")
]
