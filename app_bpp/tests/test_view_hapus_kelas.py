from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..views import hapus_kelas_view
from ..models import Kelas
from ..forms import KelasForm


class HapusKelasTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username='fillateo', password='F1ll4t30')
        self.kelas = Kelas.objects.create(nama='X')
        self.url = reverse('app_bpp:hapus_kelas', kwargs={'pk': self.kelas.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        self.assertEqual(self.response.status_code, 302)
        self.assertRedirects(self.response, reverse('app_bpp:daftar_kelas'))

    def test_successful_delete(self):
        kelas = Kelas.objects.count()
        self.assertTrue(kelas == 0)

    def test_not_found_delete(self):
        self.url = reverse('app_bpp:hapus_kelas', kwargs={'pk': 9})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)
