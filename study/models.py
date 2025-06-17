from django.db import models

class Course(models.Model):
    """
    Модель курса.
    Содержит название, описание и картинку-превью.
    """
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
