from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Course.
    Реализует полный CRUD для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """
    Контроллер для получения списка и создания уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Контроллер для получения, обновления и удаления одного урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer