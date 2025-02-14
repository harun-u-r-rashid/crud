from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone


from . import models
from . import serializers


class RegisterAPIView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def create(self, request, *args, **kwargs):
        phone = request.data["phone"]
        username = request.data["username"]
        password = request.data["password"]
        confirnm_password = request.data["confirm_password"]

        if len(password) < 6:
            return Response(
                {"message": "Password must be at least 6 characters long."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirnm_password:
            return Response(
                {"message": "Password doesn't match."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if models.User.objects.filter(phone=phone).exists():
            return Response(
                {"message": "User with this phone number already exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = models.User(phone=phone, username=username)
        user.set_password(password)
        user.save()

        return Response(
            {"message": "Your account has been registered."},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data["phone"]
        password = request.data["password"]

        user = models.User.objects.filter(phone=phone).first()

        if user is None or not user.check_password(password):
            return Response(
                {"message": "Invalid Credential."}, status=status.HTTP_404_NOT_FOUND
            )

        # if not user:
        #     return Response(
        #         {"message": "Invalid Credential."}, status=status.HTTP_404_NOT_FOUND
        #     )

        tokens = user.tokens()

        return Response(
            {
                "message": "Welcome, you're logged in.",
                "phone": phone,
                "access_token": str(tokens.get("access")),
                "refresh_token": str(tokens.get("refresh")),
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    serializer_class = serializers.LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class UpdateMembershipAPIView(generics.UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UpdateUserMembership
    permission_classes = [IsAdminUser]

    lookup_field = "pk"

    def perform_update(self, serializer):

        member_status = self.request.data.get("member_status")

        user = self.get_object()

        user.member_status = member_status
        user.member_start = timezone.now()

        if member_status == "SILVER":
            user.member_expire = timezone.now() + timedelta(days=10)
        if member_status == "DIAMOND":
            user.member_expire = timezone.now() + timedelta(days=20)
        if member_status == "GOLD":
            user.member_expire = timezone.now() + timedelta(days=30)

        user.save()

        return Response(
            {"message": "Membership activation completed."}, status=status.HTTP_200_OK
        )
