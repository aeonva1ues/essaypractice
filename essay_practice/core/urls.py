from django.urls import path

from .views import NotificationsListView

app_name = 'core'

urlpatterns = [
    path('', NotificationsListView.as_view(), name='notifications')
    ]
