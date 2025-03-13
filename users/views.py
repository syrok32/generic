from django.shortcuts import render
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


from info.serializers import PaymentSerializer
from users.models import Payment


# Create your views here.
class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    search_fields = ['paid_course', 'paid_lesson']
    ordering_fields = ['payment_date']
    filterset_fields = ['payment_method']