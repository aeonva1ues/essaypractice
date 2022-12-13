from django.db import models

from users.models import Profile


class Section(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Topic(models.Model):
    name = models.CharField(max_length=150)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                help_text='Раздел')

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'


class Essay(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_DEFAULT,
                               default='автор неизвестен')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    intro = models.TextField(help_text='Вступление')
    first_arg = models.TextField(help_text='1-ый аргумент')
    second_arg = models.TextField(help_text='2-ой аргумент')
    closing = models.TextField(help_text='Заключение')

    grades = models.ManyToManyField(
        Profile,
        through='grades.essay_grade',
        related_name='essaygrade'
        )
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'сочинение'
        verbose_name_plural = 'сочинения'
