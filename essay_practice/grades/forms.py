from django import forms
from grades.models import Essay_Grade


class RateEssayForm(forms.ModelForm):
    class Meta:
        model = Essay_Grade
        fields = (
            'relevance_to_topic', 'matching_args',
            'composition', 'speech_quality',
            'comment'
        )
