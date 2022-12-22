from django.contrib import admin
from essayfeed.models import Essay_Report


@admin.register(Essay_Report)
class EssayReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'to_essay', 'reason')
