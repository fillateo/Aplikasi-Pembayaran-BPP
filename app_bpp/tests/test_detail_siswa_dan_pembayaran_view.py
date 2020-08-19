from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Siswa, Pembayaran, Kelas, Jurusan
from ..views import detail_siswa_dan_pembayaran_view
from ..forms import PembayaranForm


class DetailSiswaDanPembayaranTestCase(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.kelas = Kelas.objects.create(nama='X')
        self.kelas2 = Kelas.objects.create(nama='XII')
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.jurusan2 = Jurusan.objects.create(nama='MM')
        self.siswa = Siswa.objects.create(nama='JRJ', kelas=self.kelas, jurusan=self.jurusan)
        self.url = reverse('app_bpp:detail_siswa', kwargs={'pk': self.siswa.pk})
        self.response = self.client.get(self.url)


class DetailSiswaDanPembayaranTest(DetailSiswaDanPembayaranTestCase):
    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, detail_siswa_dan_pembayaran_view)

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:detail_siswa', kwargs={'pk': 23234})
        self.response = self.client.get(self.url)
        self.assertEquals(self.response.status_code, 404)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PembayaranForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_inputs(self):
        self.assertContains(self.response, '<input', 4)

    def test_contain_button_submit(self):
        self.assertContains(self.response, 'type="submit"')

    def test_contain_link_back_to_home(self):
        self.assertContains(self.response, reverse('app_bpp:home'))


class SuccessfulPembayaranTest(DetailSiswaDanPembayaranTestCase):
    def test_valid_post_data(self):
        data = {
            'id_siswa': self.siswa.pk,
            'bulan_yang_dibayar': '12/2001',
            'nominal_yang_dibayar': 100000,
            'tanggal_pembayaran': '12/12/2001',
        }
        self.response = self.client.post(self.url, data)
        self.assertTrue(Pembayaran.objects.exists())
        self.assertRedirects(self.response, self.url)

    def test_invalid_post_data(self):
        data = {
            'id_siswa': self.siswa.pk,
            'bulan_yang_dibayar': '12/s2001',
            'nominal_yang_dibayar': 100000,
            'tanggal_pembayaran': '12/12/2001',
        }
        self.response = self.client.post(self.url, data)
        form = self.response.context.get('form')
        self.assertEquals(self.response.status_code, 200)
        self.assertFalse(Pembayaran.objects.exists())
        self.assertTrue(form.errors)


class LoginRequiredDetailSiswaView(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:detail_siswa', kwargs={'pk': 1})
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
