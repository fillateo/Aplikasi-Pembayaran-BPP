from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Siswa
from ..views import chart_view


class ChartTest(TestCase):
    def setUp(self):
        self.username = 'fillateo'
        self.password = 'F1ll4t30'
        User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('app_bpp:chart')
        self.response = self.client.get(self.url)

    def test_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_resolve(self):
        self.assertEquals(resolve(self.url).func, chart_view)

    def test_contains(self):
        self.assertContains(self.response, "Yang Lunas Sampai Bulan Ini")
        self.assertContains(self.response, "Jumlah Seluruh Siswa")
        self.assertContains(self.response, "Siswa yang membayar hingga bulan ini")
        self.assertContains(self.response, "Siswa yang belum membayar hingga bulan ini:")


class LoginRequiredChartTest(TestCase):
    def test_redirection(self):
        url = reverse('app_bpp:chart')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, "{}?next={}".format(login_url, url))
