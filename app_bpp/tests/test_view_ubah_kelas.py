from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import ubah_kelas_view
from ..models import Kelas
from ..forms import KelasForm


class UbahKelasTestCase(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.kelas = Kelas.objects.create(nama='X')
        self.url = reverse('app_bpp:ubah_kelas', kwargs={'pk': self.kelas.pk})
        self.response = self.client.get(self.url)


class UbahKelasTest(UbahKelasTestCase):
    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, ubah_kelas_view)

    def test_contains_link_to_daftar_kelas(self):
        self.assertContains(self.response, 'href="{}"'.format(reverse('app_bpp:daftar_kelas')))

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, KelasForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)

    def test_form_button(self):
        self.assertContains(self.response, 'type="submit"')


class SuccessfulUbahKelasTest(UbahKelasTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {'nama': 'X Changed'})

    def test_redirection(self):
        self.assertRedirects(self.response, self.url)

    def test_changed(self):
        self.kelas.refresh_from_db()
        self.assertEqual(self.kelas.nama, 'X Changed')


class InvalidUbahKelasTest(UbahKelasTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {'sdfsdf': 'df'})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
