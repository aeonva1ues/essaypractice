from django.urls import path

from .views import WritingEssayView

app_name = 'writing'

urlpatterns = [
    path('<int:pk>', WritingEssayView.as_view(), name='writing'),
]
