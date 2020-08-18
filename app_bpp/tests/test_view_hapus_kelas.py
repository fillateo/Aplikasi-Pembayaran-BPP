from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..views import hapus_kelas_view
from ..models import Kelas

class HapusKelasTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username='fillateo', password='F1ll4t30')
        self.kelas = Kelas.objects.create(nama='X')
        self.url = reverse('app_bpp:hapus_kelas', kwargs={'pk': self.kelas.pk})
        self.response = self.client.get(self.url)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, hapus_kelas_view)

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


class LoginRequiredHapusKelasTest(TestCase):
    def test_redirection(self):
        kelas = Kelas.objects.create(nama='x')
        self.url = reverse('app_bpp:hapus_kelas', kwargs={'pk': kelas.pk})
        self.login_url = reverse('accounts:login')
        self.response = self.client.get(self.url)
        self.assertRedirects(self.response, "{}?next={}".format(self.login_url, self.url))
