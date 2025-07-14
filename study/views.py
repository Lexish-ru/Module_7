from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Course, Lesson, Subscription
from .permissions import IsModerator, IsOwnerOrModerator
from .serializers import CourseSerializer, LessonSerializer
from .paginators import StandardResultsSetPagination
from users.tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Course.
    Реализует полный CRUD для курсов.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        if timezone.now() - course.updated_at > timedelta(hours=4):
            for subscription in course.subscriptions.all():
                send_course_update_email.delay(subscription.user.email, course.title)




class LessonViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для модели Lesson.
    Реализует полный CRUD для уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return queryset
        return queryset.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update", "destroy", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        sub = Subscription.objects.filter(user=user, course=course)
        if sub.exists():
            sub.delete()
            return Response({'message': 'подписка удалена'})
        else:
            Subscription.objects.create(user=user, course=course)
            return Response({'message': 'подписка добавлена'})