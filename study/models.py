from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Модель курса.
    Содержит название, описание и картинку-превью.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    title = models.CharField('Название', max_length=100)
    preview = models.ImageField('Превью', upload_to='course_previews/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        """
        Возвращает название курса.
        """
        return self.title

class Lesson(models.Model):
    """
    Модель урока.
    Принадлежит определённому курсу (ForeignKey).
    Содержит название, описание, картинку-превью и ссылку на видео.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    preview = models.ImageField('Превью', upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField('Ссылка на видео', blank=True)

    def __str__(self):
        """
        Возвращает название урока.
        """
        return self.title
