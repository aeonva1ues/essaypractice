from django.test import Client, TestCase
from django.urls import reverse_lazy

from .models import Section, Topic
from .models import Essay
from users.models import Profile
from .forms import WritingEssayForm


class TestWritingPage(TestCase):
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
        self.topic_2 = Topic.objects.create(
            name='Тема номер 2',
            section=self.section
        )
        self.topic_2.clean()
        self.topic_2.save()
        self.topic_3 = Topic.objects.create(
            name='Тема номер 3',
            section=self.section
        )
        self.topic_3.clean()
        self.topic_3.save()

    def test_writing_correct_status_code(self):
        response = Client().get(reverse_lazy('writing:writing', args=('1',)))
        self.assertEqual(response.status_code, 302)

    def test_writing_valid_form(self):
        form_data = {
            'author': self.user_1,
            'topic': self.topic_1,
            'intro': 'test ' * 250,
            'first_arg': 'test test test test test test test test test ',
            'second_arg': 'test test test test test test test test ',
            'closing': 'test test test test test test test test ',
        }

        form = WritingEssayForm(data=form_data, initial={'section': 1})

        self.assertTrue(form.is_valid())

    def test_writing_not_valid_form(self):
        form_data = {
            'author': self.user_1,
            'topic': self.topic_1,
            'intro': 'test ' * 20,
            'first_arg': 'test test test test test test test test test ',
            'second_arg': 'test test test test test test test test ',
            'closing': 'test test test test test test test test ',
        }

        form = WritingEssayForm(data=form_data, initial={'section': 1})

        self.assertFalse(form.is_valid())