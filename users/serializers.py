from rest_framework import serializers
from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для платежей
    """
    class Meta:
        model = Payment
        fields = ['id', 'user', 'date', 'course', 'lesson', 'amount', 'method', 'stripe_session_url']


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'phone', 'city', 'avatar', 'first_name', 'last_name', 'payments',]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class StripePaymentRequestSerializer(serializers.Serializer):
    """
    Сериализатор для входных данных Stripe-платежа.
    """
    course_id = serializers.IntegerField(help_text="ID курса")
    method = serializers.ChoiceField(choices=['cash', 'transfer'], default='transfer', help_text="Способ оплаты")
