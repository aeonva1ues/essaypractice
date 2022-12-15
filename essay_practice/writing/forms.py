from django.shortcuts import get_object_or_404
from django import forms
from writing.models import Essay, Topic, Section


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

    class Meta:
        model = Essay
        fields = ('topic', 'intro', 'first_arg', 'second_arg', 'closing')
