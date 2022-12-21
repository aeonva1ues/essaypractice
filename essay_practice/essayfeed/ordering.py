from django.db.models import Avg


def grade_summ(e):
    if e.grade.all():
        return e.grade.aggregate(
                    rev=Avg('relevance_to_topic'))['rev'] + \
                e.grade.aggregate(
                    matching_args=Avg('matching_args'))['matching_args'] + \
                e.grade.aggregate(
                    composition=Avg('composition'))['composition'] + \
                e.grade.aggregate(
                    speech_quality=Avg('speech_quality'))['speech_quality']
    return 0
