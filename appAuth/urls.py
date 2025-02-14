from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    #    User authentication
    path("register/", views.RegisterAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("logout/", views.LogoutAPIView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    # Update User membership
    path("member/update/<int:pk>/", views.UpdateMembershipAPIView.as_view()),
]
