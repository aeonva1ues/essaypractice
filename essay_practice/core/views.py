from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from .models import Notification

'''
Является ли пользователь админом
'''


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class NotificationsListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'core/notifications.html'
    paginate_by = 3
    context_object_name = 'notifications'

    def get_queryset(self):
        return (
            Notification.objects
            .filter(to_who__id=self.request.user.id)
            .order_by('-pub_date')
            .only('text', 'status', 'pub_date')
        )
