from rest_framework import routers

from backend.users.views import UserRegisterViewSet, LoginViewSet, ResetPasswordViewSet

user_router = routers.DefaultRouter()

user_router.register(r"registry", UserRegisterViewSet, basename="registry")
user_router.register(r"login", LoginViewSet, basename="login")
user_router.register(r"reset_password", ResetPasswordViewSet, basename="reset_password")
