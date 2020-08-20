from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogInTests(TestCase):
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
