from writing.models import Section
from core.models import Notification


def all_sections(request):
    sections = Section.objects.all()
    return {'all_sections': sections}


def unread_messages(request):
    if request.user.is_authenticated:
        notfs = Notification.objects.filter(
            to_who=request.user,
            is_read=False).only('id').all()
        return {'notifications_count': len(notfs)}
    else:
        return {'notifications_count': -1}
