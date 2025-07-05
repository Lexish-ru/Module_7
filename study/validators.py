from rest_framework import serializers

class YoutubeUrlValidator:
    """Валидатор: пропускает только youtube.com, можно использовать в DRF-сериализаторе."""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value and 'youtube.com' not in value:
            raise serializers.ValidationError('Можно добавлять только ссылки на youtube.com')

    def __repr__(self):
        return f'<YoutubeUrlValidator(field={self.field})>'
