from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, SubscriptionAPIView

app_name = "study"

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),  # /api/courses/
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),  # /api/lessons/
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),  # /api/lessons/<id>/
    path('subscribe/', SubscriptionAPIView.as_view(), name='subscribe'), # /api/subscribe/
]
