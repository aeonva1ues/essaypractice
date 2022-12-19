from django.test import TestCase

from writing.models import Section, Topic
from writing.models import Essay
from users.models import Profile
from .forms import RateEssayForm


class TestGrades(TestCase):
    def setUp(self):
        super().setUpClass()
        self.user_1 = Profile.objects.create(
            username='Test Person',
            email='test@test.ru',
            password='test0test0test'
        )
        self.section = Section.objects.create(name='Секция номер 1')
        self.section.clean()
        self.section.save()
        self.topic_1 = Topic.objects.create(
            name='Тема номер 1',
            section=self.section
        )
        self.topic_1.clean()
        self.topic_1.save()

        self.essay = Essay.objects.create(
            author=self.user_1,
            topic=self.topic_1,
            intro='test '*251,
            first_arg='test',
            second_arg='test',
            closing='test'
        )
        self.essay.clean()
        self.essay.save()

    def test_grades_valid_form(self):
        form_data = {
            'reviewer': self.user_1,
            'essay': self.essay,
            'relevance_to_topic': 2,
            'matching_args': 2,
            'composition': 1,
            'speech_quality': 2,
            'comment': 'test comment',
        }

        form = RateEssayForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_grades_not_valid_form(self):
        form_data = {
            'reviewer': self.user_1,
            'essay': self.essay,
            'relevance_to_topic': 2,
            'speech_quality': 2,
            'comment': 'test comment',
        }

        form = RateEssayForm(data=form_data)

        self.assertFalse(form.is_valid())
