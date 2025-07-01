from rest_framework import serializers

def youtube_only_validator(value):
    """
    Валидатор: разрешает только ссылки на youtube.com
    """
    if value and "youtube.com" not in value:
        raise serializers.ValidationError("Разрешены только ссылки на youtube.com")
    return value
