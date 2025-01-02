from django.urls import path, include
# from rest_framework_nested import routers
from .views import *


urlpatterns = [
    path("jwt/create/", CustomObtainPairView.as_view(), name="customtoken"),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('verify/<int:user_id>/', VerifyUserApiView.as_view(), name='user-verify'),
    path("profile/", UserProfileDetail.as_view(), name="user-profile"),


]
