from django.test import Client, TestCase
from django.urls import reverse_lazy

from users.models import Profile

from .forms import WritingEssayForm
from .models import Section, Topic, Essay


class TestWritingPage(TestCase):
    def setUp(self):
        super().setUpClass()
        self.user_1 = Profile.objects.create(
            username='Test Person',
            email='test@test.ru',
            password='test0test0test'
        )
        self.user_2 = Profile.objects.create(
            username='Test Person2',
            email='test2@test.ru',
            password='test0test0test'
        )
        self.user_3 = Profile.objects.create(
            username='Test Person3',
            email='test3@test.ru',
            password='test0test0test'
        )
        self.user_4 = Profile.objects.create(
            username='Test Person4',
            email='test4@test.ru',
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

        self.essay = Essay.objects.create(
            author=self.user_2,
            topic=self.topic_1,
            intro='intro. test! a?' * 20,
            first_arg='f.i.r.s.t!' * 50,
            second_arg='SECOND! ARG.' * 20,
            closing='closing. clooosing. clooooosing' * 20
        )
        self.essay.clean()
        self.essay.save()

    def test_writing_correct_status_code(self):
        response = Client().get(reverse_lazy('writing:writing',
                                             args=('1',)))
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

        form = WritingEssayForm(
            data=form_data, instance=self.user_1,
            initial={'section': 1, 'last_topic': None})

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

        form = WritingEssayForm(
            data=form_data, instance=self.user_1,
            initial={'section': 1, 'last_topic': None})

        self.assertFalse(form.is_valid())

    def context_processor_test(self):
        response = Client().get(reverse_lazy(
            'writing:writing', args=('1',)))
        self.assertIn(
            'all_sections',
            response.context,
            'в контекст не передано all_sections')

        self.assertEqual(
            response.context['all_sections'],
            Section.objects.all(),
            'в all_sections лежит что-то не то')

    def test_antiplagiat_negative(self):
        form_data = {
            'author': self.user_3,
            'topic': self.topic_1,
            'intro': 'intro. test! a?' * 20,
            'first_arg': 'fi.rs.t.ar.g?' * 20,
            'second_arg': 'SECOND! ARG.' * 20,
            'closing': 'closing. clooosing. clooooosing' * 20,
        }
        form = WritingEssayForm(
            data=form_data, instance=self.user_3,
            initial={'section': 1, 'last_topic': None})

        self.assertFalse(form.is_valid())

    def test_antiplagiat_positive(self):
        form_data = {
            'author': self.user_4,
            'topic': self.topic_1,
            'intro': 'test test test test test test test test test .',
            'first_arg': 'ы? ыы.ы.ы.ыыы.' * 20,
            'second_arg': 'SECOND. arg. second_arg.' * 20,
            'closing': 'cl.os.ing. ccc. lll. ooo. sing' * 60,
        }
        form = WritingEssayForm(
            data=form_data, instance=self.user_4,
            initial={'section': 1, 'last_topic': None})

        try:
            form.full_clean()
        except Exception as e:
            print(e)

        self.assertTrue(form.is_valid())
