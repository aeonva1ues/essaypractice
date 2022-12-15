from django.urls import path
from essayfeed.views import essay_feed


app_name = 'essayfeed'

urlpatterns = [
    path('', essay_feed, name='feed')
]
