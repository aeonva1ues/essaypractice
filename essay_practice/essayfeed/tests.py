from django.test import Client, TestCase
from django.urls import reverse_lazy

from writing.models import Section, Topic
from writing.models import Essay
from users.models import Profile


class TestFeedPage(TestCase):
    def setUp(self):
        super().setUpClass()
        self.user_1 = Profile.objects.create(
            username='Test Person Yep',
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

    def test_feed_correct_status_code(self):
        '''
        Главная лента
        '''
        response = Client().get(reverse_lazy('essayfeed:feed'))
        self.assertEqual(response.status_code, 200)

    def test_my_essays_correct_status_code(self):
        '''
        Мои сочинения
        '''
        response = Client().get(reverse_lazy('essayfeed:my_essays'))
        self.assertEqual(response.status_code, 302)

    def test_detail_essay_status_code(self):
        '''
        Просмотр сочинения
        '''
        response = Client().get(reverse_lazy('essayfeed:detail_essay',
                                             args=('1',)))
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = Client().get(reverse_lazy('essayfeed:feed'))
        self.assertEqual(response.context['paginator'].num_pages, 1)


class TestModerationReports(TestCase):
    def setUp(self):
        super().setUpClass()
        self.pwd = 'test0test0test'
        self.client = Client()
        self.admin = Profile.objects.create_superuser(
            username='Bos',
            email='admin@test.ru',
            password=self.pwd,
        )
        self.just_user = Profile.objects.create(
            username='bober',
            email='justbober@test.ru',
            password=self.pwd
        )

    def test_reports_page_for_admin(self):
        '''
        Администратор открывает страницу с жалобами
        '''
        self.client.login(email=self.admin.email, password=self.pwd)
        response = self.client.get(reverse_lazy('essayfeed:check-reports'))
        self.assertEqual(response.status_code, 200)

    def test_reports_page_for_user(self):
        '''
        Простой пользователь открывает страницу с жалобами
        '''
        self.client.login(email=self.just_user.email, password=self.pwd)
        response = self.client.get(reverse_lazy('essayfeed:check-reports'))
        self.assertEqual(response.status_code, 302)
