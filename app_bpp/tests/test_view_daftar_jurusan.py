from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..views import list_jurusan_view
from ..models import Jurusan
from ..forms import JurusanForm


class TestDaftarJurusan(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('app_bpp:daftar_jurusan')
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)
