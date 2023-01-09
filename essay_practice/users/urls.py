from django.contrib.auth import views
from django.urls import path

from users.views import (
    ChangeUserProfileView, SignUpView, ConfirmSignUpView,
    CancelSignUpView
)

app_name = 'users'

urlpatterns = [
    path(
        'login/',
        views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change.html'
            ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        views.PasswordResetView.as_view(
            template_name='users/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('signup/', SignUpView.as_view(), name='signup'),
    path(
        'change-profile-info/',
        ChangeUserProfileView.as_view(),
        name='change-profile'
    ),
    path(
        'activate/<uidb64>/<token>/',
        ConfirmSignUpView.as_view(), name='activate'),
    path(
        'cancel-registration/<uidb64>/<token>/',
        CancelSignUpView.as_view(), name='cancel_registration'),
]
