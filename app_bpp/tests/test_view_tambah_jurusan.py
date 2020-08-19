from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import tambah_jurusan_view
from ..models import Jurusan
from ..forms import JurusanForm


class TambahJurusanTests(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('app_bpp:tambah_jurusan')

    def test_valid_post_data(self):
        jurusan = {
            'nama': 'TKJ'
        }
        response = self.client.post(self.url, jurusan)
        redirect_url = reverse('app_bpp:daftar_jurusan')
        self.assertRedirects(response, redirect_url)
        self.assertTrue(Jurusan.objects.count() == 1)

    def test_invalid_post_data(self):
        response = self.client.post(self.url, {'sdf': 'sffjl'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Jurusan.objects.count() == 0)


class LoginRequiredTambahJurusanTests(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:tambah_jurusan')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
