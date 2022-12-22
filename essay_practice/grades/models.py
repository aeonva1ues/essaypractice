from django.db import models

from users.models import Profile
from writing.models import Essay


class Essay_Grade(models.Model):
    reviewer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='grade',
        verbose_name='оценено пользователем')

    essay = models.ForeignKey(
        Essay,
        on_delete=models.CASCADE,
        related_name='grade',
        verbose_name='сочинение')

    GRADE_CHOICES = (0, '0'), (1, '1'), (2, '2')

    relevance_to_topic = models.IntegerField(
        choices=GRADE_CHOICES,
        verbose_name='соответствие теме')

    matching_args = models.IntegerField(
        choices=GRADE_CHOICES,
        verbose_name='аргументация')

    composition = models.IntegerField(
        choices=GRADE_CHOICES,
        verbose_name='композиция')

    speech_quality = models.IntegerField(
        choices=GRADE_CHOICES,
        verbose_name='качество речи')

    comment = models.TextField(verbose_name='комментарий')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации')

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
        constraints = [
            models.UniqueConstraint(
                fields=['reviewer', 'essay'],
                name='unique reviewer_essay pair'
            )
        ]
