from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
import re

from users.models import Profile
from writing.models import Essay, Section, Topic


class WritingEssayForm(forms.ModelForm):
    section = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
        label=''
    )

    def __init__(self, *args, **kwargs):
        super(WritingEssayForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.name == 'mentors_email':
                '''
                Полю mentors_email необходимо передать не только form-control,
                но и visually-hidden, поскольку оно изначально скрыто
                (до нажатия галочки)
                '''
                field.field.widget.attrs['class'] = (
                    'visually-hidden '
                    'form-control'
                )
            else:
                field.field.widget.attrs['class'] = 'form-control'
            field.field.widget.attrs['style'] = 'border-left-color: black'
            field.field.widget.attrs['placeholder'] = field.field.label
        if not kwargs['initial']['last_topic']:
            section = get_object_or_404(
                Section, id=kwargs['initial']['section'])
            topics = Topic.objects.filter(section=section).order_by('?')
            self.fields['topic'].queryset = topics
        else:
            self.fields['topic'].queryset = Topic.objects.filter(
                id=kwargs['initial']['last_topic'])

        self.author = kwargs['instance']

    class Meta:
        model = Essay
        fields = (
            'topic', 'intro', 'first_arg',
            'second_arg', 'closing', 'mentors_email'
        )

    def clean(self):
        '''
        Объем сочинения должен превышать 250 слов
        '''
        if (
            len(self.cleaned_data['intro'].split()) +
            len(self.cleaned_data['first_arg'].split()) +
            len(self.cleaned_data['second_arg'].split()) +
            len(self.cleaned_data['closing'].split())
        ) < 250:
            raise ValidationError('Сочинение не прошло по объему.')

        '''
        КД между отправками сочинений - 20 минут
        '''
        last = self._meta.model.objects.order_by(
            'pub_date').filter(author=self.author).only('pub_date').last()
        if last:
            if timezone.now() - last.pub_date < timezone.timedelta(minutes=20):
                raise ValidationError(
                    'Вы подозрительно быстро пишете сочинения!')
        self.pub_date = timezone.now()

        '''
        Если указали почту ментора - проверить существует ли она
        '''
        if self.cleaned_data['mentors_email']:
            if self.instance.email == self.cleaned_data['mentors_email']:
                raise ValidationError(
                    'Вы не можете отправить сочинение самому себе'
                )
            users = Profile.objects.filter(
                email=self.cleaned_data['mentors_email'])
            if not users:
                raise ValidationError(
                    'Аккаунта с указанной почтой не существует, '
                    'проверьте корректность введенных данных'
                )
        '''
        Проверка на плагиат
        (сравнивается с другими сочинениями на сайте с такой же темой)
        '''
        essays = Essay.objects.filter(
            topic=self.cleaned_data['topic']
            ).only('intro', 'first_arg', 'second_arg', 'closing').all()
        essay = set(re.split(
            '().?!',
            (self.cleaned_data['intro'] +
             self.cleaned_data['first_arg'] +
             self.cleaned_data['second_arg'] +
             self.cleaned_data['closing']).lower()))
        plagiated = 0
        for e in essays:
            plagiated += len(set(re.split('().?!', (e.intro +
                                 e.first_arg + e.second_arg +
                                 e.closing).lower())) & essay)
        originality = 100 - plagiated / len(essay) * 100
        if originality < 30:
            raise ValidationError(f'Оригинальность - {originality}%')
