from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from djoser.serializers import UserCreateSerializer as BaseUCS
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
import random,string
from .models import Referral

class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        user = User.objects.filter(email=attrs["email"])
        if not user.exists():
            raise exceptions.AuthenticationFailed(
                "No account found with this email. Create an account now."
            )

        user = user.first()

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                "Your account has not been activated."
            )

        if not user.check_password(attrs["password"]):
            raise exceptions.AuthenticationFailed("Your password is incorrect.")

        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


User = get_user_model()

class UserShortInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "email","username"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password','id']
        extra_kwargs = {'password': {'write_only': True},'id':{'read_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        ref = Referral(user = user, code=''.join(random.choices(string.ascii_lowercase, k=2)) + str(user.id) + ''.join(random.choices(string.ascii_lowercase, k=2)))
        ref.save()
        return user
