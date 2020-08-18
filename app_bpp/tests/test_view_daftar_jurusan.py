from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import list_jurusan_view
from ..models import Jurusan
from ..forms import JurusanForm


class DaftarJurusanTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('app_bpp:daftar_jurusan')
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, list_jurusan_view)

    def test_contains_link_to_daftar_jurusan(self):
        self.assertContains(self.response, 'href="{}"'.format(self.url))

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, JurusanForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_inputs(self):
        self.assertContains(self.response, '<input', 2)

    def test_contain_button(self):
        self.assertContains(self.response, 'type="submit"', 1)

    def test_contain_list_of_jurusan(self):
        daftar_jurusan = self.response.context.get('daftar_jurusan')
        self.assertTrue(daftar_jurusan.count() == 0)


class LoginRequiredDaftarJurusanTest(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:daftar_jurusan')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
