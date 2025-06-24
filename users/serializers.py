from rest_framework import serializers
from .models import CustomUser, Payment



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'date', 'course', 'lesson', 'amount', 'method']


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name', 'payments']