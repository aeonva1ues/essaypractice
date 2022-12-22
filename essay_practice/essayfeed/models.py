from django.db import models

from writing.models import Essay
from users.models import Profile


class Essay_Report(models.Model):
    '''
    Жалобы на сочинение, оставленные пользователями
    '''
    class Meta:
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'

    def __str__(self):
        return f'Жалоба #{self.id}'

    from_user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sended_reports',
        verbose_name='оставлена пользователем'
    )
    to_essay = models.ForeignKey(
        Essay,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='сочинение с нарушением'
    )

    REASON_CHOICES = (
        (0, 'Оффтоп/Спам'),
        (1, 'Пропаганда/Реклама'),
        (2, 'Нецензурная лексика')
    )

    reason = models.IntegerField(
        choices=REASON_CHOICES,
        verbose_name='нарушение'
    )

    report_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата жалобы'
    )
