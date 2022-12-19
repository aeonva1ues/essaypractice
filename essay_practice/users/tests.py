from django.test import Client, TestCase
from django.urls import reverse_lazy


class TestUsers(TestCase):
    def setUp(self):
        super().setUpClass()

    def test_login_correct_status_code(self):
        response = Client().get(reverse_lazy('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_correct_status_code_and_redirect(self):
        response = Client().get(reverse_lazy('users:logout'))
        self.assertRedirects(
            response,
            reverse_lazy('users:login'),
        )
        self.assertEqual(response.status_code, 302)

    def test_password_change_correct_status_code(self):
        response = Client().get(reverse_lazy('users:password_change'))
        self.assertEqual(response.status_code, 302)

    def test_password_change_done_correct_status_code(self):
        response = Client().get(reverse_lazy('users:password_change_done'))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_correct_status_code(self):
        response = Client().get(reverse_lazy('users:password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_correct_status_code(self):
        response = Client().get(reverse_lazy('users:password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm_correct_status_code(self):
        response = Client().get(reverse_lazy('users:password_reset_confirm',
                                             args=('123', '123')))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_correct_status_code(self):
        response = Client().get(reverse_lazy('users:password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_signup_correct_status_code(self):
        response = Client().get(reverse_lazy('users:signup'))
        self.assertEqual(response.status_code, 200)

    def test_change_profile_correct_status_code(self):
        response = Client().get(reverse_lazy('users:change-profile'))
        self.assertEqual(response.status_code, 302)
