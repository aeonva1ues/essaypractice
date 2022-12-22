from django.db import models

from users.models import Profile


class Notification(models.Model):
    to_who = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name='получатель')

    text = models.TextField(verbose_name='текст')

    status = models.CharField(
        choices=(('D', 'danger'), ('S', 'success'),
                 ('W', 'warning'), ('I', 'info')),
        max_length=1,
        verbose_name='статус',
        help_text='на сочинение получена жалоба. статус сочинения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации')

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'
