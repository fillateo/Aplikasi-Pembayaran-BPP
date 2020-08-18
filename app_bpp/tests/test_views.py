from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..views import *
from ..models import Kelas
from ..forms import KelasForm, SiswaForm, JurusanForm, PembayaranForm


class DaftarKelasTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('app_bpp:daftar_kelas')
        user = User.objects.create(username='fillateo')
        user.set_password('F1ll4t30')
        user.save()
        self.client.login(username='fillateo', password='F1ll4t30')
        Kelas.objects.create(nama='X').save()
        self.response = self.client.get(self.url)

    def test_daftar_kelas_url_resolves(self):
        self.assertEquals(resolve(self.url).func, list_kelas_view)

    def test_daftar_kelas_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_daftar_kelas_contains_link_to_ubah_kelas_page(self):
        ubah_kelas_url = reverse('app_bpp:ubah_kelas', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{}"'.format(ubah_kelas_url))

    def test_daftar_kelas_contains_link_to_hapus_kelas_page(self):
        hapus_kelas_url = reverse('app_bpp:hapus_kelas', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{}"'.format(hapus_kelas_url))


class TambahKelasTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('app_bpp:tambah_kelas')
        user = User.objects.create(username='fillateo')
        user.set_password('F1ll4t30')
        user.save()
        self.client.login(username='fillateo', password='F1ll4t30')
        self.response = self.client.get(self.url)

    def test_tambah_kelas_url_resolves(self):
        self.assertEqual(resolve(self.url).func, tambah_kelas_view)

    def test_tambah_kelas_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tambah_kelas_contains_link_to_daftar_kelas(self):
        daftar_kelas_url = reverse('app_bpp:daftar_kelas')
        self.assertContains(self.response, 'href="{}"'.format(daftar_kelas_url))

    def test_tambah_kelas_contains_form(self):
        self.assertIsInstance(self.response.context.get('form'), KelasForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_add_new_kelas_valid_data(self):
        kelas = {
            'nama': 'X',
        }
        post_response = self.client.post(self.url, kelas)
        self.assertEqual(Kelas.objects.first().nama, 'X')
        self.assertEqual(post_response.status_code, 302)

    def test_add_new_kelas_invalid_data(self):
        post_response = self.client.post(self.url, {})
        self.assertEqual(Kelas.objects.count(), 0)
        self.assertEqual(post_response.status_code, 200)
