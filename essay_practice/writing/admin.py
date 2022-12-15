from django.contrib import admin
from writing.models import Essay, Topic, Section


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')
    list_filter = ('section',)
    search_fields = ('name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'author', 'topic')
