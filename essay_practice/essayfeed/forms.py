from django import forms

from essayfeed.models import Essay_Report, CommentReport


class ReportEssayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportEssayForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Essay_Report
        fields = ('reason',)


class ReportCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportCommentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = CommentReport
        fields = ('reason',)
