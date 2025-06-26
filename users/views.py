from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Payment
from .serializers import PaymentSerializer

class PaymentListView(generics.ListAPIView):
    """
    Эндпоинт для получения списка платежей с возможностью фильтрации и сортировки.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['date']
    ordering = ['-date']
