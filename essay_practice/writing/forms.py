from django import forms
from .models import Essay, Topic


class WritingEssayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WritingEssayForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.order_by('?')[:3]

    class Meta:
        model = Essay
        fields = ('topic', 'intro', 'first_arg', 'second_arg', 'closing')
