from django.urls import path
from rest_framework.routers import DefaultRouter

from info.views import CourListAPIView, CourCreateAPIView, LessonViewSet, CourRetrieveAPIView, CourDestroyAPIView, \
    CourUpdateAPIView

app_name = 'info'

router = DefaultRouter()

router.register(r'lessons', LessonViewSet, basename='lesson')  # Измените базовое имя
urlpatterns = [
                  path('cours/create/', CourCreateAPIView.as_view(), name='cors-cr'),
                  path('cours/', CourListAPIView.as_view(), name='cours-list'),
                  path('cours/destroy/<int:pk>/', CourDestroyAPIView.as_view(), name='cours-des'),
                  path('cours/<int:pk>/', CourRetrieveAPIView.as_view(), name='cours-det'),
                  path('cours/update/<int:pk>/', CourUpdateAPIView.as_view(), name='cours-det'),
              ] + router.urls
