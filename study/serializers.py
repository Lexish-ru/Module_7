from rest_framework import serializers
from .models import Course, Lesson
from .validators import youtube_only_validator


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    video_url = serializers.URLField(validators=[youtube_only_validator])
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели курса
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()