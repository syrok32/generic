from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from users.models import Payment
from info.models import Cours, Lesson
from info.serializers import LessonSerializer, CoursSerializer, PaymentSerializer

# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class CourCreateAPIView(generics.CreateAPIView):
    serializer_class = CoursSerializer


class CourListAPIView(generics.ListAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()


class CourRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()

class CourUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()

class CourDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CoursSerializer
    queryset = Cours.objects.all()




