from writing.models import Section
from core.models import Notification

from django.contrib.auth.decorators import login_required


def all_sections(request):
    sections = Section.objects.all()
    return {'all_sections': sections}


@login_required
def unread_messages(request):
    notfs = Notification.objects.filter(
        to_who=request.user,
        is_read=False).only('id').all()
    return {'notifications_count': len(notfs)}
