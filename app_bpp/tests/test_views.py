from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..views import list_kelas_view
from ..models import Kelas


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
