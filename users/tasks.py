from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_course_update_email(user_email, course_title):
    send_mail(
        f'Обновление курса "{course_title}"',
        f'В курсе "{course_title}" появились новые материалы!',
        'from@example.com',
        [user_email]
    )
