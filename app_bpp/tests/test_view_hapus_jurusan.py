from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..models import Jurusan



class HapusJurusanTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.url = reverse('app_bpp:hapus_jurusan', kwargs={'pk': self.jurusan.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('app_bpp:daftar_jurusan'))

    def test_successful_delete_siswa(self):
        self.assertTrue(Jurusan.objects.count() == 0)

    def test_successful_delete_pembayaran(self):
        self.assertFalse(Jurusan.objects.filter(pk=self.jurusan.pk).exists())

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:hapus_jurusan', kwargs={'pk': 1111})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)


class LoginRequiredHapusJurusanTest(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:hapus_jurusan', kwargs={'pk': 1})
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
