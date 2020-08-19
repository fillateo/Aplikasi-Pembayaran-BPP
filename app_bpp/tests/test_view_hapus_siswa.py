from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.utils import timezone
from ..models import Siswa, Kelas, Jurusan, Pembayaran


class HapusSiswaTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.kelas = Kelas.objects.create(nama='X')
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.siswa = Siswa.objects.create(nama='JRJ', kelas=self.kelas, jurusan=self.jurusan)
        self.pembayaran = Pembayaran.objects.create(id_siswa=self.siswa.pk,
                                    bulan_yang_dibayar=timezone.now().date(),
                                    nominal_yang_dibayar=100000,
                                    tanggal_pembayaran=timezone.now().date())
        self.url = reverse('app_bpp:hapus_siswa', kwargs={'pk': self.siswa.pk})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('app_bpp:daftar_siswa'))

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:hapus_kelas', kwargs={'pk': 134})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_successful_delete_siswa(self):
        self.assertFalse(Siswa.objects.exists())

    def test_successful_delete_pembayaran_if_exists(self):
        self.assertFalse(Pembayaran.objects.filter(id_siswa=self.siswa.pk).exists())
