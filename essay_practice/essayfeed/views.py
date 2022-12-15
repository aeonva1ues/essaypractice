from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from writing.models import Essay
from grades.models import Essay_Grade
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404


class EssayListView(ListView):
    model = Essay
    template_name = 'essay_feed/feed.html'
    paginate_by = 2
    context_object_name = 'essays'


class EssayDetailView(DetailView):
    model = Essay
    template_name = 'essay_feed/detail_essay.html'
    context_object_name = 'essay'

    def get_queryset(self):
        self.pk = self.kwargs.get(self.pk_url_kwarg)

        essay = get_object_or_404(Essay, pk=self.pk)
        print(essay.grades.prefetch_related(Prefetch('grades', queryset=Essay_Grade.objects.all().filter(essay__pk=self.kwargs.get('pk')))))
        essay.essaygrade.all()
        print(essay.grades.all())

        # essay = (
        #     Essay.objects.filter(pk=self.pk).prefetch_related(
        #         Prefetch(
        #             'grades',
        #             queryset=Essay_Grade.objects.all().filter(essay__pk=self.kwargs.get('pk'))
        #         )
        #     )
        # )

        return essay