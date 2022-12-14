import numpy as np

from django import forms
from .models import Essay, Topic

class WritingEssayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WritingEssayForm, self).__init__(*args, **kwargs)
        data = Topic.objects.all().only('name', 'section__pk')
        print(len(Topic.objects.all()))
        self.fields['topic'].queryset = Topic.objects.filter(pk__in=np.random.randint(1, len(Topic.objects.all()), 6))

    class Meta:
        model = Essay
        fields = ('topic', 'intro', 'first_arg', 'second_arg', 'closing')
