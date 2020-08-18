from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Siswa, Kelas, Jurusan
from ..views import home_view


class HomeTestCase(TestCase):
    def setUp(self):
        self.url = reverse('app_bpp:home')
        kelas = Kelas.objects.create(nama='X')
        jurusan = Jurusan.objects.create(nama='TKJ')
        Siswa.objects.create(nama='Siswa', kelas=kelas, jurusan=jurusan).save()
        self.username = "fillateo"
        self.password = "F1ll4t30"
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEquals(resolve(self.url).func, home_view)

    def test_contains_link_to_detail_siswa(self):
        detail_siswa_url = reverse('app_bpp:detail_siswa', kwargs={'pk': 1})
        self.assertContains(self.response, 'href="{}"'.format(detail_siswa_url))
