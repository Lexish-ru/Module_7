from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'first_name', 'last_name']
