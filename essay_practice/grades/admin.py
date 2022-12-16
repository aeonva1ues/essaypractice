from django.contrib import admin
from .models import Essay_Grade


@admin.register(Essay_Grade)
class EssayGradeAdmin(admin.ModelAdmin):
    list_display = (
        'reviewer', 'essay', 'relevance_to_topic',
        'matching_args', 'composition', 'speech_quality',
        'comment', 'pub_date')
