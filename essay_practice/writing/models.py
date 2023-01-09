from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from core.models import Notification
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

    mentors_email = models.EmailField(
        'почта получателя', blank=True, null=True)

    grades = models.ManyToManyField(
        Profile,
        through='grades.essay_grade',
        related_name='essaygrade',
        verbose_name='оценки'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации')

    class Meta:
        verbose_name = 'сочинение'
        verbose_name_plural = 'сочинения'

    def __str__(self):
        return f'Сочинение "{self.topic}"'

    def delete(self, *args, **kwargs):
        Notification(
            to_who=self.author,
            text='Ваше сочинение было удалено модератором по жалобе(-ам)!',
            status='D'
        ).save()

        mail_subject = 'Ваше сочинение на EssayPractice было удалено'
        message = render_to_string('writing/delete_essay_msg.html', {
            'user': self.author
        })
        to_email = self.author.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        super(Essay, self).delete(*args, **kwargs)
