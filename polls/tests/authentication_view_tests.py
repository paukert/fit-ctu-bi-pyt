from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


def create_user():
    return User.objects.create_user(username='Lukas', password='SecretPassword')


class AuthenticationSignUpViewTests(TestCase):
    def test_redirect_if_logged_in(self):
        create_user()
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:signup'))
        self.assertEqual(response.status_code, 302)

    def test_signup_ok(self):
        response = self.client.post(reverse('polls:signup'), {
            'username': 'Lukas',
            'password1': 'SecretPassword',
            'password2': 'SecretPassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_signup_fail(self):
        response = self.client.post(reverse('polls:signup'), {
            'username': 'Lukas',
            'password1': 'SecretPassword',
            'password2': 'SecretPassword1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(auth.get_user(self.client).is_authenticated)


class AuthenticationLogInViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_user()

    def test_redirect_if_logged_in(self):
        self.client.login(username='Lukas', password='SecretPassword')
        response = self.client.get(reverse('polls:login'))
        self.assertEqual(response.status_code, 302)

    def test_login_ok(self):
        response = self.client.post(reverse('polls:login'), {
            'username': 'Lukas',
            'password': 'SecretPassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_login_fail(self):
        response = self.client.post(reverse('polls:login'), {
            'username': 'Lukas',
            'password': 'SecretPassword1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(auth.get_user(self.client).is_authenticated)


class AuthenticationLogOutViewTests(TestCase):
    def test_response(self):
        response = self.client.get(reverse('polls:logout'))
        self.assertEqual(response.status_code, 302)
