from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from grades.models import Essay_Grade
from users.token import account_activation_token
from users.forms import ChangeProfileInfoForm, SignUpForm
from users.models import Profile


class SignUpView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password1'])
        new_user.is_active = False
        new_user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Активация аккаунта на EssayPractice'
        message = render_to_string('users/create_account.html', {
            'user': new_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.id)),
            'token': account_activation_token.make_token(new_user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(
            self.request,
            'На вашу почту было отправлено письмо с подтверждением!')

        return super().form_valid(form)


class ConfirmSignUpView(TemplateView):
    template_name = 'users/check_activation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (
            user is not None and
                account_activation_token.check_token(
                    user, self.kwargs['token'])):
            user.is_active = True
            user.save()
            msg = 'Вы успешно зарегистрировались!'
            status = True
        else:
            msg = 'Вы воспользовались невалидной ссылкой!'
            status = False

        context['msg'] = msg
        context['status'] = status
        return context


class CancelSignUpView(TemplateView):
    template_name = 'users/cancel_registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (
            user is not None and
                account_activation_token.check_token(
                    user, self.kwargs['token']) and
                not user.is_active):
            user.delete()
            msg = 'Регистрация была отменена'
        else:
            msg = 'Вы воспользовались невалидной ссылкой!'

        context['msg'] = msg
        return context


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
