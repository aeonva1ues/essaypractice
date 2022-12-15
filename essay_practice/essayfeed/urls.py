from django.urls import path
from essayfeed.views import EssayListView, EssayDetailView


app_name = 'essayfeed'

urlpatterns = [
    path('', EssayListView.as_view(), name='feed'),
    path('essay/<int:pk>/', EssayDetailView.as_view(), name='detail_essay'),
]
