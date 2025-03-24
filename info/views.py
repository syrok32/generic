from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from info.models import Cours, Lesson, Subscription
from info.paginators import MyPagination
from info.serializers import LessonSerializer, CoursSerializer
from users.permissions import UserPermissions, IsOwner


# Create your views here.

class SubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        cuors_fk = request.data.get('cuors_fk')
        user_fk = request.user

        course_item = get_object_or_404(Cours, id=cuors_fk)

        subs_item = Subscription.objects.filter(user_fk=user_fk, cuors_fk=cuors_fk)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
            # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user_fk=user_fk, cuors_fk=course_item)
            message = 'подписка добавлена'
            # Возвращаем ответ в API

        return Response({"message": message})


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Привязываем текущего пользователя к создаваемому объекту
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            print('dd')
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
    pagination_class = MyPagination


class CourRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()
    permission_classes = (IsAuthenticated | UserPermissions | IsOwner,)


class CourUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()
    permission_classes = (IsAuthenticated | UserPermissions | IsOwner,)


class CourDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~UserPermissions)
