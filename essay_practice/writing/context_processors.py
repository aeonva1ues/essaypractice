from writing.models import Section


def all_sections(request):
    sections = Section.objects.all()
    return {'all_sections': sections}
