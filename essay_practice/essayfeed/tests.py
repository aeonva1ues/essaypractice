from django.test import Client, TestCase
from django.urls import reverse_lazy


class TestFeedPage(TestCase):
    def test_feed_correct_status_code(self):
        response = Client().get(reverse_lazy('essayfeed:feed'))
        self.assertEqual(response.status_code, 200)

    def test_my_essays_correct_status_code(self):
        response = Client().get(reverse_lazy('essayfeed:my_essays'))
        self.assertEqual(response.status_code, 302)
