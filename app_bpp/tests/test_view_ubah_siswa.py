from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Siswa, Pembayaran, Kelas, Jurusan
from ..views import ubah_siswa_view
from ..forms import SiswaForm


class UbahSiswaTestCase(TestCase):
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
        self.pembayaran = Pembayaran.objects.create(id_siswa=self.siswa.pk,
                                    bulan_yang_dibayar=timezone.now().date(),
                                    nominal_yang_dibayar=100000,
                                    tanggal_pembayaran=timezone.now().date())
        self.url = reverse('app_bpp:ubah_siswa', kwargs={'pk': self.siswa.pk})
        self.response = self.client.get(self.url)


class UbahSiswaTest(UbahSiswaTestCase):
    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'app_bpp/form_siswa.html')


    def test_resolve(self):
        self.assertEquals(resolve(self.url).func, ubah_siswa_view)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SiswaForm)

    def test_contains_inputs(self):
        self.assertContains(self.response, '<input', 2)

    def test_contain_option(self):
        kelas_options = Kelas.objects.count()
        jurusan_options = Jurusan.objects.count()
        self.assertContains(self.response, '<option', kelas_options + jurusan_options + 2)

    def test_contain_button_submit(self):
        self.assertContains(self.response, 'type="submit"')

    def test_not_found_status_code(self):
        self.url = reverse('app_bpp:ubah_siswa', kwargs={'pk': 30234})
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 404)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SuccessfulUbahSiswaTest(UbahSiswaTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
                'nama': 'Nama Changed',
                'kelas': self.kelas2.pk,
                'jurusan': self.jurusan2.pk,
                }
        self.response = self.client.post(self.url, self.data)

    def test_redirection(self):
        self.assertRedirects(self.response, self.url)

    def test_siswa_changed(self):
        self.siswa.refresh_from_db()
        self.assertEqual(self.siswa.nama, self.data['nama'])
        self.assertEqual(self.siswa.kelas.pk, self.data['kelas'])
        self.assertEqual(self.siswa.jurusan.pk, self.data['jurusan'])


class InvalidUbahSiswaTest(UbahSiswaTestCase):
    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {'sdfsd': 'sdfsdf'})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)


class LoginRequiredUbahSiswa(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:ubah_siswa', kwargs={'pk': 234234})
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
