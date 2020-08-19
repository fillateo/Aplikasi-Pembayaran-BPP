from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Pembayaran, Siswa, Kelas, Jurusan
from ..views import ubah_riwayat_pembayaran_view
from ..forms import PembayaranForm
from django.utils import timezone


class UbahRiwayatPembayaranTestCase(TestCase):
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
        self.url = reverse('app_bpp:ubah_riwayat_pembayaran', kwargs={
                                                                'id_siswa': self.siswa.pk,
                                                                'pk': self.pembayaran.pk,
                                                            })
        self.response = self.client.get(self.url)


class UbahRiwayatPembayaranTest(UbahRiwayatPembayaranTestCase):
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
        self.url = reverse('app_bpp:ubah_riwayat_pembayaran', kwargs={
                                                                'id_siswa': self.siswa.pk,
                                                                'pk': self.pembayaran.pk,
                                                            })
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEquals(resolve(self.url).func, ubah_riwayat_pembayaran_view)

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:ubah_riwayat_pembayaran', kwargs={
                                                                'id_siswa': 2342,
                                                                'pk': 1231,
                                                            })
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PembayaranForm)

    def test_contains_inputs(self):
        self.assertContains(self.response, '<input', 4)

    def test_contains_button(self):
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SuccessfulUbahRiwayatPembayaranTest(UbahRiwayatPembayaranTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, data = {
            'id_siswa': self.siswa.pk,
            'bulan_yang_dibayar': '12/2001',
            'nominal_yang_dibayar': 100000,
            'tanggal_pembayaran': '12/12/2001',
        })


    def test_redirection(self):
        self.assertRedirects(self.response, reverse('app_bpp:detail_siswa', kwargs={'pk': self.siswa.pk}))

    def test_data_changed(self):
        self.pembayaran.refresh_from_db()
        self.assertTrue(self.pembayaran.bulan_yang_dibayar != timezone.now())


class InvalidUbahRiwayatPembayaranTest(UbahRiwayatPembayaranTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {
            'id_siswa': self.siswa.pk,
            'bulan_yang_dibayar': 'sdfds12/2001',
            'nominal_yang_dibayar': 32100000,
            'tanggal_pembayaran': 'sdf12/12/2001',
        })

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)


    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class LoginRequiredUbahRiwayatPembayaranView(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:ubah_riwayat_pembayaran', kwargs={'id_siswa': 1, 'pk': 1})
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
