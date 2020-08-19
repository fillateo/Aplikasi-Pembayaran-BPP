from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Pembayaran, Siswa, Kelas, Jurusan
from ..views import hapus_riwayat_pembayaran_view
from django.utils import timezone


class HapusRiwayatPembayaranTestCase(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.kelas = Kelas.objects.create(nama='X')
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.siswa = Siswa.objects.create(nama='JRJ', kelas=self.kelas, jurusan=self.jurusan)
        self.pembayaran = Pembayaran.objects.create(id_siswa=self.siswa.id,
                                                    bulan_yang_dibayar=timezone.now().date(),
                                                    nominal_yang_dibayar=100000,
                                                    tanggal_pembayaran=timezone.now().date())
        self.url = reverse('app_bpp:hapus_riwayat_pembayaran', kwargs={
                                                                'id_siswa': self.siswa.pk,
                                                                'pk': self.pembayaran.pk,
                                                            })
        self.response = self.client.get(self.url)

    def test_resolve(self):
        self.assertEquals(resolve(self.url).func, hapus_riwayat_pembayaran_view)

    def test_delete_success(self):
        self.assertRedirects(self.response, reverse('app_bpp:detail_siswa', kwargs={'pk': self.siswa.pk}))
        self.assertFalse(Pembayaran.objects.exists())

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:hapus_riwayat_pembayaran', kwargs={
                                                                'id_siswa': 1231,
                                                                'pk': 12312,
                                                            })
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)


class LoginRequiredHapusRiwayatPembayaranView(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:hapus_riwayat_pembayaran', kwargs={'id_siswa': 1, 'pk': 1})
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
