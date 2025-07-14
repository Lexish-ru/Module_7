from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

@shared_task
def send_course_update_email(user_email, course_title):
    send_mail(
        f'Обновление курса "{course_title}"',
        f'В курсе "{course_title}" появились новые материалы!',
        'from@example.com',
        [user_email]
    )

@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(is_active=True, last_login__lt=month_ago)
    users.update(is_active=False)