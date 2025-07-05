from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from study.models import Course, Lesson, Subscription

class CourseCRUDAndPermissionsTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.owner = self.User.objects.create_user(email='owner2@test.com', password='ownerpass')
        self.other = self.User.objects.create_user(email='other2@test.com', password='otherpass')
        self.client.force_authenticate(self.owner)
        self.course = Course.objects.create(title="Курс владельца", owner=self.owner)

    def test_owner_can_create_course(self):
        url = reverse('study:course-list')
        data = {'title': 'Мой новый курс'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_owner_can_edit_own_course(self):
        url = reverse('study:course-detail', args=[self.course.id])
        response = self.client.patch(url, {'title': 'Изменён'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit_someone_else_course(self):
        self.client.force_authenticate(self.other)
        url = reverse('study:course-detail', args=[self.course.id])
        response = self.client.patch(url, {'title': 'Хак!'}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_owner_can_delete_own_course(self):
        url = reverse('study:course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_other_user_cannot_delete_someone_else_course(self):
        self.client.force_authenticate(self.other)
        url = reverse('study:course-detail', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_list_and_retrieve_course(self):
        url = reverse('study:course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data['results']), 1)
        url = reverse('study:course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_retrieve_course(self):
        self.client.force_authenticate(self.other)
        url = reverse('study:course-detail', args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class LessonCRUDAndPermissionsTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.owner = self.User.objects.create_user(email='owner@test.com', password='ownerpass')
        self.other = self.User.objects.create_user(email='other@test.com', password='otherpass')
        self.course = Course.objects.create(title="Курс владельца", owner=self.owner)
        self.lesson = Lesson.objects.create(title="Урок владельца", course=self.course, owner=self.owner, video_url='https://youtube.com/test')
        self.client.force_authenticate(self.owner)

    def test_owner_can_create_lesson(self):
        url = reverse('study:lesson-list')
        data = {
            'title': 'Новый урок',
            'course': self.course.id,
            'video_url': 'https://youtube.com/new'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_owner_can_edit_own_lesson(self):
        url = reverse('study:lesson-detail', args=[self.lesson.id])
        response = self.client.patch(url, {'title': 'Изменён'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Изменён')

    def test_other_user_cannot_edit_someone_else_lesson(self):
        self.client.force_authenticate(self.other)
        url = reverse('study:lesson-detail', args=[self.lesson.id])
        response = self.client.patch(url, {'title': 'Хак!'}, format='json')
        self.assertEqual(response.status_code, 404)

    def test_owner_can_delete_own_lesson(self):
        url = reverse('study:lesson-detail', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_other_user_cannot_delete_someone_else_lesson(self):
        self.client.force_authenticate(self.other)
        url = reverse('study:lesson-detail', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

class SubscriptionTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(email='testuser@test.com', password='pass')
        self.course = Course.objects.create(title="Курс для подписки", owner=self.user)
        self.client.force_authenticate(self.user)

    def test_subscribe(self):
        url = reverse('study:subscribe')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('study:subscribe')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())