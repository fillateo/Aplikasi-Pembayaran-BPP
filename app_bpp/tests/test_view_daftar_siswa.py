from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Siswa, Pembayaran, Kelas, Jurusan
from ..views import list_siswa_view
from ..forms import SiswaForm


class DaftarSiswaTest(TestCase):
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
        self.url = reverse('app_bpp:daftar_siswa')
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, list_siswa_view)

    def test_contains_link_to_tambah_siswa(self):
        self.assertContains(self.response, 'href="{}"'.format(reverse('app_bpp:tambah_siswa')))


class LoginRequiredDaftarSiswa(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:daftar_siswa')
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
