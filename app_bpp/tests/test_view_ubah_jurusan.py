from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import ubah_jurusan_view
from ..models import Jurusan
from ..forms import JurusanForm


class UbahJurusanTestCase(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.url = reverse('app_bpp:ubah_jurusan', kwargs={'pk': self.jurusan.pk})
        self.response = self.client.get(self.url)


class UbahJurusanTest(UbahJurusanTestCase):

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, ubah_jurusan_view)

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:ubah_jurusan', kwargs={'pk': 1000})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, JurusanForm)

    def test_contains_inputs(self):
        self.assertContains(self.response, '<input', 2)

    def test_contains_button(self):
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_link_to_daftar_jurusan(self):
        daftar_jurusan_url = reverse('app_bpp:daftar_jurusan')
        self.assertContains(self.response, 'href="{}"'.format(daftar_jurusan_url))


class SuccessfulUbahJurusanTest(UbahJurusanTestCase):
        def setUp(self):
            super().setUp()
            self.response = self.client.post(self.url, {'nama': 'Jurusan diganti'})


        def test_redirection(self):
            daftar_jurusan_url = reverse('app_bpp:daftar_jurusan')
            self.assertRedirects(self.response, daftar_jurusan_url)


        def test_changed(self):
            self.jurusan.refresh_from_db()


class InvalidUbahJurusanTest(UbahJurusanTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {'sdfsdf': 'sdfsd'})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class LoginRequiredUbahJurusan(TestCase):
    def test_redirection(self):
        login_url = reverse('accounts:login')
        url = reverse('app_bpp:ubah_jurusan', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
