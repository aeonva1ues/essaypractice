from django import forms
from .models import Essay_Grade


class RateEssayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RateEssayForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Essay_Grade
        fields = (
            'relevance_to_topic', 'matching_args',
            'composition', 'speech_quality',
            'comment'
        )
