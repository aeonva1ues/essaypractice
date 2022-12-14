from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView

from users.models import Profile

from .forms import WritingEssayForm
from .models import Essay


class WritingEssayView(LoginRequiredMixin, FormView):
    template_name = 'writing/writing_essay.html'
    form_class = WritingEssayForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.cleaned_data['author'] = Profile.objects.get(
            pk=self.request.user.pk
        )
        essay = Essay.objects.create(**form.cleaned_data)
        essay.save()
        return super().form_valid(form)
