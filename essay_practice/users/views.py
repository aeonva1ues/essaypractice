from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from grades.models import Essay_Grade
from users.forms import ChangeProfileInfoForm, SignUpForm
from users.models import Profile


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.save()
        return super().form_valid(form)


class ChangeUserProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/change_profile.html'
    form_class = ChangeProfileInfoForm
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        self.user_profile = Profile.objects.get(id=self.request.user.id)
        form_class = ChangeProfileInfoForm(
            self.request.POST or None,
            instance=self.user_profile,
        )
        return form_class

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Поле изменено!')
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        profile_info = (
            Profile.objects
            .filter(id=user_id)
            .first()
        )
        context['user'] = profile_info
        context['review_count'] = Essay_Grade.objects.filter(
                                        essay__author__id=user_id)
        return context
