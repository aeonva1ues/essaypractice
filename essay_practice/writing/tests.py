from django.test import Client, TestCase
from django.urls import reverse_lazy

# from .models import Section, Topic, Essay
# from users.models import Profile
# from .forms import WritingEssayForm


class TestWritingPage(TestCase):
    def setUp(self):
        super().setUpClass()
        self.form = WritingEssayForm()
        self.user_1 = Profile.objects.create(
            username='Test Person',
            email='test@test.ru',
            password='test0test0test'
        )
        self.section = Section.objects.create(name='Секция номер 1')
        self.section.clean()
        self.section.save()
        self.topic_1 = Topic.objects.create(name='Тема номер 1', section=self.section)
        self.topic_1.clean()
        self.topic_1.save()
        self.topic_2 = Topic.objects.create(name='Тема номер 2', section=self.section)
        self.topic_2.clean()
        self.topic_2.save()
        self.topic_3 = Topic.objects.create(name='Тема номер 3', section=self.section)
        self.topic_3.clean()
        self.topic_3.save()

    def test_writing_correct_status_code(self):
        response = Client().get(reverse_lazy('writing:writing', args=('1',)))
        self.assertEqual(response.status_code, 302)

    # def test_writing_contains_form(self):
    #     essays_count = Essay.objects.count()
    #     form_data = {
    #         'author': self.user_1,
    #         'topic': self.topic_1,
    #         'intro': ' test test test test test test test test test ',
    #         'first_arg': 'test test test test test test test test test test ',
    #         'second_arg': 'test test test test test test test test ',
    #         'closing': 'test test test test test test test test ',
    #     }
    #
    #     response = Client().post(
    #         reverse_lazy('writing:writing', args=('1',)),
    #         data=form_data,
    #         follow=True
    #     )
    #
    #     self.assertEqual(
    #         Essay.objects.count(),
    #         essays_count + 1,
    #     )
    #     self.assertTrue(
    #         Essay.objects.filter(
    #             topic=self.topic_1
    #         ).exists()
    #     )
