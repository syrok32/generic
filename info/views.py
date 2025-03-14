from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from info.models import Cours, Lesson
from info.serializers import LessonSerializer, CoursSerializer
from users.permissions import UserPermissions, IsOwner


# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Привязываем текущего пользователя к создаваемому объекту
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            # Для create и destroy используем IsAuthenticated и UserPermissions
            self.permission_classes = (~UserPermissions,)
        elif self.action in ['update', 'retrieve']:
            # Для update и retrieve используем только UserPermissions
            self.permission_classes = (UserPermissions | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (~UserPermissions | IsOwner,)
        return super().get_permissions()


class CourCreateAPIView(generics.CreateAPIView):
    serializer_class = CoursSerializer
    permission_classes = (~UserPermissions, IsAuthenticated,)

    def perform_create(self, serializer):
        # Привязываем текущего пользователя к создаваемому объекту
        serializer.save(user=self.request.user)


class CourListAPIView(generics.ListAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()


class CourRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()
    permission_classes = (IsAuthenticated |UserPermissions | IsOwner,)

class CourUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()
    permission_classes = (IsAuthenticated | UserPermissions | IsOwner,)

class CourDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()
    permission_classes = (IsAuthenticated, IsOwner |  ~UserPermissions)
