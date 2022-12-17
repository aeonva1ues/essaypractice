from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
            field.field.widget.attrs['class'] = 'form-control'
            field.field.widget.attrs['style'] = 'border-left-color: black'
            field.field.widget.attrs['placeholder'] = field.field.label

        section = get_object_or_404(Section, id=kwargs['initial']['section'])
        topics = Topic.objects.filter(section=section).order_by('?')
        self.fields['topic'].queryset = topics

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

        last = self._meta.model.objects.order_by(
            'pub_date').only('pub_date').last()
        print(last)
        if last.pub_date - timezone.now() < timezone.timedelta(minutes=20):
            raise ValidationError('Вы подозрительно быстро пишете сочинения!')

    class Meta:
        model = Essay
        fields = ('topic', 'intro', 'first_arg', 'second_arg', 'closing')
