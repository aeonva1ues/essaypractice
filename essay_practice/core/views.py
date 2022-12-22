from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


'''
Является ли пользователь админом
'''


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
