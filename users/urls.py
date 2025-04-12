from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import (
    PaymentListAPIView,
    UserCreateAPIView,
    UserDeleteAPIView,
    UserUpdateAPIView,
    UserRetrieveAPIView,
    UserListAPIView,
    PaymentCreateAPIView,
)

app_name = "users"
urlpatterns = [
    path("pay/", PaymentListAPIView.as_view(), name="pay"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="token_obtain_pair",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("delete/<int:pk>", UserDeleteAPIView.as_view(), name="delete"),
    path("list/", UserListAPIView.as_view(), name="list"),
    path("update/<int:pk>", UserUpdateAPIView.as_view(), name="update"),
    path("retriew/<int:pk>", UserRetrieveAPIView.as_view(), name="retr"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="create-payment"),
]
