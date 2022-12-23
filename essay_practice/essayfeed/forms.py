from django import forms

from essayfeed.models import Essay_Report


class ReportEssayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportEssayForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Essay_Report
        fields = ('reason',)
