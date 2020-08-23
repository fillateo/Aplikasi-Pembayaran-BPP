from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Siswa, Pembayaran, Kelas, Jurusan
from ..views import tambah_siswa_view
from ..forms import SiswaForm


class DaftarSiswaTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.kelas = Kelas.objects.create(nama='X')
        self.jurusan = Jurusan.objects.create(nama='TKJ')
        self.url = reverse('app_bpp:tambah_siswa')
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEqual(resolve(self.url).func, tambah_siswa_view)

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

    def test_valid_post_data(self):
        data = {
            'nama': 'Jait',
            'kelas': self.kelas.pk,
            'jurusan': self.jurusan.pk,
        }
        self.response = self.client.post(self.url, data)
        self.assertTrue(Siswa.objects.first().nama == 'Jait')
        self.assertTrue(Siswa.objects.first().kelas == self.kelas)
        self.assertTrue(Siswa.objects.first().jurusan == self.jurusan)
        self.assertRedirects(self.response, self.url)

    def test_invalid_post_data(self):
        from django.contrib.messages import get_messages

        self.response = self.client.post(self.url, {'sdfsdf': 'sdfsfd'})
        messages = list(get_messages(self.response.wsgi_request))
        self.assertTrue(Siswa.objects.count() == 0)
        self.assertEquals(self.response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Gagal menambahkan data!')

class LoginRequiredTambahSiswa(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:tambah_siswa')
        response = self.client.get(url)
        login_url = reverse('accounts:login')
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
