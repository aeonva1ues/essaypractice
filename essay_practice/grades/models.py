from django.db import models

from users.models import Profile
from writing.models import Essay


class Essay_Grade(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    essay = models.ForeignKey(
        Essay,
        on_delete=models.CASCADE,
        verbose_name='Сочинение')

    relevance_to_topic = models.IntegerField(
        choices=((0, '0'), (1, '1'), (2, '2')),
        verbose_name='Соответствие теме')

    matching_args = models.IntegerField(
        choices=((0, '0'), (1, '1'), (2, '2')),
        verbose_name='Аргументация')

    composition = models.IntegerField(
        choices=((0, '0'), (1, '1'), (2, '2')),
        verbose_name='Композиция')

    speech_quality = models.IntegerField(
        choices=((0, '0'), (1, '1'), (2, '2')),
        verbose_name='Качество речи')

    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
