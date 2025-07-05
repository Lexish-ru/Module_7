from rest_framework import serializers
from .models import Course, Lesson
from .validators import YoutubeUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    video_url = serializers.URLField(
        required=False, allow_blank=True,
        validators=[YoutubeUrlValidator(field='video_url')]
    )
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.subscriptions.filter(user=user).exists()
