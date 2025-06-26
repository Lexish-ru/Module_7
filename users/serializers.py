from rest_framework import serializers
from .models import CustomUser, Payment



class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для платежей
    """
    class Meta:
        model = Payment
        fields = ['id', 'user', 'date', 'course', 'lesson', 'amount', 'method']


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    password = serializers.CharField(write_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name', 'payments']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user