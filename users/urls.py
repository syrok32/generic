from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import PaymentListAPIView, UserCreateAPIView

app_name = 'users'
urlpatterns = [
    path('pay/', PaymentListAPIView.as_view(), name='pay'),
    path('login/', TokenObtainPairView.as_view(permission_classes = [AllowAny]), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register')
]
