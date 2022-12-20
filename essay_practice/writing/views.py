from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from users.models import Profile

from writing.forms import WritingEssayForm
from writing.models import Essay


class WritingEssayView(LoginRequiredMixin, FormView):
    template_name = 'writing/writing_essay.html'
    form_class = WritingEssayForm
    success_url = reverse_lazy('essayfeed:my_essays')

    def get_form(self, form_class=None):
        self.user_profile = Profile.objects.get(id=self.request.user.id)
        form_class = WritingEssayForm(
            self.request.POST or None,
            instance=self.user_profile,
            initial={
                'section': self.kwargs['pk'],
                'last_topic': self.request.POST.get('topic')
            }
        )
        return form_class

    def form_valid(self, form):
        form.cleaned_data['author'] = Profile.objects.get(
            pk=self.request.user.pk
        )
        form.cleaned_data.pop('section')  # вспомогательное hidden поле
        essay = Essay.objects.create(**form.cleaned_data)
        essay.save()
        return super().form_valid(form)
