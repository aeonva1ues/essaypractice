from django.db import models

from users.models import Profile
from writing.models import Essay
from grades.models import Essay_Grade


REASON_CHOICES = (
        (0, 'Оффтоп/Спам'),
        (1, 'Пропаганда/Реклама'),
        (2, 'Нецензурная лексика')
    )


class Essay_Report(models.Model):
    '''
    Жалобы на сочинение, оставленные пользователями
    '''
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

    reason = models.IntegerField(
        choices=REASON_CHOICES,
        verbose_name='нарушение'
    )

    report_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата жалобы'
    )

    class Meta:
        verbose_name = 'жалоба'
        verbose_name_plural = 'жалобы'

    def __str__(self):
        return f'Жалоба #{self.id}'


class CommentReport(models.Model):
    '''
    Жалоба на комментарий под сочинением
    '''
    from_user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='автор жалобы'
    )
    comment = models.ForeignKey(
        Essay_Grade,
        on_delete=models.CASCADE,
        verbose_name='комментарий с нарушением'
    )
    reason = models.IntegerField(
        choices=REASON_CHOICES,
        verbose_name='нарушение'
    )
    report_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата жалобы'
    )

    class Meta:
        verbose_name = 'жалоба на комментарий'
        verbose_name_plural = 'жалобы на комментарии'

    def __str__(self):
        return f'Жалоба #{self.id} на комментарий'
