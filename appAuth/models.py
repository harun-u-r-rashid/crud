from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from rest_framework_simplejwt.tokens import RefreshToken

from .constants import MEMBER_STATUS


class AccountManager(BaseUserManager):
    def create_user(
        self,
        phone,
        username,
        password=None,
    ):
        if not phone:
            raise ValueError("User must have a phone number.")
        user = self.model(
            phone=phone,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password):
        user = self.create_user(
            phone=phone,
            username=username,
            password=password,
        )

        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=30, unique=True)
    username = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # Membership fields

    member_status = models.CharField(
        max_length=100, choices=MEMBER_STATUS, default="SILVER"
    )
    member_start = models.DateTimeField(blank=True, null=True)
    member_expire = models.DateTimeField(blank=True, null=True)

    refresh_token = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    def __str__(self):
        return self.phone

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
