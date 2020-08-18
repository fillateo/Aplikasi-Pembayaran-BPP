from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import tambah_kelas_view
from ..models import Kelas
from ..forms import KelasForm


class LoginRequiredTambahKelasTests(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:tambah_kelas')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, "{}?next={}".format(login_url, url))


class TambahKelasTests(TestCase):
    def setUp(self):
        self.url = reverse('app_bpp:tambah_kelas')
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_resolve(self):
        self.assertEquals(resolve(self.url).func, tambah_kelas_view)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_contains_link_to_daftar_kelas(self):
        daftar_kelas_url = reverse('app_bpp:daftar_kelas')
        self.assertContains(self.response, 'href="{}"'.format(daftar_kelas_url))

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, KelasForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)

    def test_form_button(self):
        self.assertContains(self.response, 'type="submit"', 1)

    def test_new_kelas_valid_data(self):
        kelas = {
            'nama': 'X',
        }
        self.response = self.client.post(self.url, kelas)
        self.assertEqual(Kelas.objects.first().nama, 'X')
        self.assertRedirects(self.response, reverse('app_bpp:daftar_kelas'))

    def test_new_kelas_invalid_data(self):
        self.response = self.client.post(self.url, {})
        self.assertEquals(self.response.status_code, 200)
        self.assertTrue(Kelas.objects.count() == 0)
