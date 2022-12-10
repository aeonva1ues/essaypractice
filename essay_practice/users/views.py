from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from users.forms import ChangeProfileInfoForm, SignUpForm
from users.models import Profile


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    form_class = ChangeProfileInfoForm
    success_url = reverse_lazy('users:profile')

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
