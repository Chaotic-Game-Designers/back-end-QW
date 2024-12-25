from django.urls import path, include
# from rest_framework_nested import routers
from .views import *

router = SimpleRouter()
router.register("profile", views.UserProfileViewSet)

urlpatterns = [
    path("jwt/create/", CustomObtainPairView.as_view(), name="customtoken"),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('verify/<int:user_id>/', VerifyUserApiView.as_view(), name='user-verify'),
    path("", include(router.urls)),


]
