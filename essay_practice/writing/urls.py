from django.urls import path

from .views import WritingEssayView

app_name = 'writing'

urlpatterns = [
    path('', WritingEssayView.as_view(), name='writing'),
]
