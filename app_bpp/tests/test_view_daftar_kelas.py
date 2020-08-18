from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import list_kelas_view
from ..forms import KelasForm
from ..models import Kelas


class LoginRequiredDaftarKelasTest(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:daftar_kelas')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response,  "{}?next={}".format(login_url, url))


class DaftarKelasTest(TestCase):
    def setUp(self):
        self.url = reverse("app_bpp:daftar_kelas")
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.client.login(username=self.username, password=self.password)
        self.assertEquals(self.response.status_code, 200)

    def test_resolve(self):
        view = resolve(self.url)
        self.assertEqual(view.func, list_kelas_view)

    def test_contains_daftar_kelas(self):
        daftar_kelas = self.response.context.get('daftar_kelas')
        self.assertEquals(daftar_kelas.count(), Kelas.objects.all().count())

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, KelasForm)

    def test_contains_inputs(self):
        self.assertContains(self.response, '<input')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
