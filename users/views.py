from rest_framework import generics, viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from services.stripe_service import create_stripe_product, create_stripe_price, create_stripe_session
from study.models import Course
from .models import Payment, CustomUser
from .serializers import PaymentSerializer, UserSerializer, StripePaymentRequestSerializer

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

class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD для пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserRegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class StripePaymentView(APIView):
    """
    API endpoint для создания платежа через Stripe.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=StripePaymentRequestSerializer)
    def post(self, request):
        course_id = request.data.get('course_id')
        method = request.data.get('method', 'transfer')
        course = get_object_or_404(Course, id=course_id)
        amount = float(course.price)

        product = create_stripe_product(course.title)
        price = create_stripe_price(product.id, amount)
        session = create_stripe_session(
            price.id,
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel"
        )

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=amount,
            method=method,
            stripe_session_url=session.url
        )

        serializer = PaymentSerializer(payment)
        return Response({
            "payment": serializer.data,
            "stripe_url": session.url
        })
