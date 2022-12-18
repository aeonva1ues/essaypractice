from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from users.models import Profile


class Section(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='название раздела')

    class Meta:
        verbose_name = 'раздел'
        verbose_name_plural = 'разделы'

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='название темы')

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        help_text='раздел',
        verbose_name='раздел')

    class Meta:
        verbose_name = 'тема'
        verbose_name_plural = 'темы'

    def __str__(self):
        return self.name


class Essay(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_DEFAULT,
        default='автор неизвестен',
        verbose_name='автор комментария')

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name='тема')

    intro = models.TextField(
        help_text='Вступление',
        verbose_name='вступление')

    first_arg = models.TextField(
        help_text='1-ый аргумент',
        verbose_name='1-ый аргумент')

    second_arg = models.TextField(
        help_text='2-ой аргумент',
        verbose_name='2-ой аргумент')

    closing = models.TextField(
        help_text='Заключение',
        verbose_name='заключение')

    grades = models.ManyToManyField(
        Profile,
        through='grades.essay_grade',
        related_name='essaygrade',
        verbose_name='оценки'
        )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'сочинение'
        verbose_name_plural = 'сочинения'

    def clean(self):
        last = self._meta.model.objects.order_by(
            'pub_date').only('pub_date').exclude(pk=self.pk).last()
        if last:
            if last.pub_date - timezone.now() < timezone.timedelta(minutes=20):
                raise ValidationError(
                    'Вы подозрительно быстро пишете сочинения!')
        self.pub_date = timezone.now()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Сочинение "{self.topic}"'
