from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'fillateo',
            'password': 'F1ll4t30'
        }
        User.objects.create_user(**self.credentials)

    def test_login(self):
        url = reverse('accounts:login')
        response = self.client.post(url, self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_redirect_if_authenticated(self):
        self.client.login(username=self.credentials['username'], password=self.credentials['password'])
        url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response,  reverse('app_bpp:home'))

    def test_invalid_login(self):
        from django.contrib.messages import get_messages

        self.client.login(username='salah', password='salah')
        url = reverse('accounts:login')
        response = self.client.post(url, {'username': 'salah', 'password': 'salah'}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Nama pengguna/Kata sandi salah!')

    def test_logout(self):
        url = reverse('accounts:logout')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('accounts:login'))
