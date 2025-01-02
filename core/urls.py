from django.urls import path, include
# from rest_framework_nested import routers
from .views import *
from rest_framework.routers import SimpleRouter

from . import views

rouer = SimpleRouter()
rouer.register("profile", views.UserProfileViewSet)

urlpatterns = [
    path("jwt/create/", CustomObtainPairView.as_view(), name="customtoken"),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('verify/<int:user_id>/', VerifyUserApiView.as_view(), name='user-verify'),
    path("", include(rouer.urls)),
]
