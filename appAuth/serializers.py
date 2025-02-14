from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


from . import models

class RegistrationSerializer(serializers.ModelSerializer):
        confirm_password = serializers.CharField(required=True)

        class Meta:
                model = models.User
                fields = ["phone", "username", "password", "confirm_password"]
        


class LoginSerializer(serializers.ModelSerializer):
        phone = serializers.CharField(max_length=100, write_only=True)
        password = serializers.CharField(max_length=100, write_only=True)
        access_token = serializers.CharField(max_length=255, read_only=True)
        refresh_token = serializers.CharField(max_length=255, read_only=True)

        class Meta:
                model = models.User
                fields = ["phone", "password", "access_token", "refresh_token"]



class LogoutSerializer(serializers.Serializer):
        refresh_token = serializers.CharField()

        def validate(self, attrs):
                self.token = attrs.get("refresh_token")
                return attrs
        
        def save(self, **kwargs):
                try:
                        token = RefreshToken(self.token)
                        token.blacklist()
                
                except TokenError:
                        return self.fail("Bad Token.")
                



class UpdateUserMembership(serializers.ModelSerializer):
             class Meta:
                     model = models.User
                     fields = ["member_status"]          