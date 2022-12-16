from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from writing.models import Essay
from grades.models import Essay_Grade
from grades.forms import RateEssayForm


class EssayListView(ListView):
    model = Essay
    template_name = 'essay_feed/feed.html'
    paginate_by = 10
    context_object_name = 'essays'


class EssayDetailView(FormMixin, DetailView):
    model = Essay
    template_name = 'essay_feed/detail_essay.html'
    form_class = RateEssayForm
    context_object_name = 'essay'

    def get_object(self):
        self.pk = self.kwargs.get(self.pk_url_kwarg)
        self.essay = (
            Essay.objects
            .prefetch_related(
                Prefetch(
                    'grade',
                    Essay_Grade.objects.all().filter(essay__id=self.pk)
                )
            )
            .filter(id=self.pk)
            .first()
        )

        self.user_grade = (
            self.essay.grade
            .filter(reviewer__id=self.request.user.id)
            .only(
                'relevance_to_topic', 'matching_args',
                'composition', 'speech_quality',
                'comment')
            .first()
        )
        return self.essay

    def get_success_url(self):
        return reverse_lazy(
            'essayfeed:detail_essay',
            kwargs={'pk': self.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_initial(self):
        '''
        Если пользователь уже оценивал сочинение - подставить
        '''
        if self.user_grade:
            return (
                {
                    'relevance_to_topic': self.user_grade.relevance_to_topic,
                    'matching_args': self.user_grade.matching_args,
                    'composition': self.user_grade.composition,
                    'speech_quality': self.user_grade.speech_quality,
                    'comment': self.user_grade.comment
                }
            )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        Essay_Grade.objects.update_or_create(
            reviewer=self.request.user,
            essay=self.essay,
            defaults={
                'relevance_to_topic': form.cleaned_data['relevance_to_topic'],
                'matching_args': form.cleaned_data['matching_args'],
                'composition': form.cleaned_data['composition'],
                'speech_quality': form.cleaned_data['speech_quality'],
                'comment': form.cleaned_data['comment']
            }
        )
        return super(EssayDetailView, self).form_valid(form)
