from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .permissions import IsModerator, IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Course.
    Реализует полный CRUD для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator & ~IsModerator]
        elif self.action in ['update', 'partial_update', 'retrieve', 'list']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonListCreateView(generics.ListCreateAPIView):
    """
    Контроллер для получения списка и создания уроков.
    """
    permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrModerator]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Контроллер для получения, обновления и удаления одного урока.
    """
    permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrModerator]
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer