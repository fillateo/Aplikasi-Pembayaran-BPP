from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..models import Jurusan, Pembayaran, Kelas, Siswa
from django.utils import timezone



class HapusJurusanTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.kelas = Kelas.objects.create(nama='Y')
        self.siswa = Siswa.objects.create(nama='Z', kelas=self.kelas, jurusan=self.jurusan)
        self.pembayaran = Pembayaran.objects.create(id_siswa=self.siswa.pk,
                                    bulan_yang_dibayar=timezone.now().date(),
                                    nominal_yang_dibayar=100000,
                                    tanggal_pembayaran=timezone.now().date())
        self.url = reverse('app_bpp:hapus_jurusan', kwargs={'pk': self.jurusan.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('app_bpp:daftar_jurusan'))

    def test_successful_delete_siswa(self):
        self.assertTrue(Jurusan.objects.count() == 0)

    def test_successful_delete_jurusan(self):
        self.assertFalse(Jurusan.objects.filter(pk=self.jurusan.pk).exists())

    def test_successful_delete_pembayaran_if_exists(self):
        self.assertFalse(Pembayaran.objects.exists())

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
