from django.db.models import Avg, Prefetch
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from writing.models import Essay
from grades.models import Essay_Grade
from grades.forms import RateEssayForm


class EssayListView(ListView):
    model = Essay
    template_name = 'essay_feed/feed.html'
    paginate_by = 5
    context_object_name = 'essays'

    def get_queryset(self):
        essays_feed = (
            Essay.objects
            .prefetch_related(
                Prefetch(
                    'grade',
                    Essay_Grade.objects.all()
                )
            )
            .order_by('-pub_date')
        ).filter(mentors_email='')
        return essays_feed


class MyEssaysListView(LoginRequiredMixin, EssayListView):
    def get_queryset(self):
        return (
            Essay.objects
            .select_related('author')
            .filter(author__id=self.request.user.id)
        )


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
                    Essay_Grade.objects.all()
                    .filter(essay__id=self.pk)
                    .order_by('-pub_date')
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
                'comment'
            )
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
        if self.request.user.id is None:
            context.pop('form')
        if self.request.user.id == self.essay.author.id:
            messages.info(self.request, 'Вы смотрите свое сочинение')
            context.pop('form')
        if self.essay.grade.all():
            avg_relevance_to_topic = (
                self.essay.grade
                .aggregate(rev=Avg(
                    'relevance_to_topic'))['rev'] / 2 * 100
            )
            avg_matching_args = (
                self.essay.grade
                .aggregate(
                    matching_args=Avg(
                        'matching_args'))['matching_args'] / 2 * 100
            )
            avg_composition = (
                self.essay.grade
                .aggregate(
                    composition=Avg(
                        'composition'))['composition'] / 2 * 100
            )
            avg_speech_quality = (
                self.essay.grade
                .aggregate(speech=Avg(
                    'speech_quality'))['speech'] / 2 * 100
            )
        else:
            avg_relevance_to_topic = '-'
            avg_matching_args = '-'
            avg_composition = '-'
            avg_speech_quality = '-'

        context['avg_relevance_to_topic'] = avg_relevance_to_topic
        context['avg_matching_args'] = avg_matching_args
        context['avg_composition'] = avg_composition
        context['avg_speech_quality'] = avg_speech_quality
        essay_volume = (
            len(self.essay.intro.strip().split()) +
            len(self.essay.first_arg.strip().split()) +
            len(self.essay.second_arg.strip().split()) +
            len(self.essay.closing.strip().split())
        )
        context['volume'] = essay_volume
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
            messages.success(request, 'Спасибо за ваше ревью!')
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


class ReceivedEssays(ListView):
    model = Essay
    template_name = 'essay_feed/feed.html'
    paginate_by = 5
    context_object_name = 'essays'

    def get_queryset(self):
        essays_feed = (
            Essay.objects
            .prefetch_related(
                Prefetch(
                    'grade',
                    Essay_Grade.objects.all()
                )
            )
            .order_by('-pub_date')
        ).filter(mentors_email=self.request.user.email)
        return essays_feed
