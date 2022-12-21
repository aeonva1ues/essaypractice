from django.template import Library
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


def order(essays, n):
    if n == 0:
        return sorted(essays, key=lambda e: -e.pub_date)
    return sorted(
        essays,
        key=lambda e: -grade_summ(e))


register = Library()
register.filter('order', order)
