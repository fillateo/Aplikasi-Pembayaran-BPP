from django.test import TestCase
from django.utils import timezone
from ..models import Kelas, Jurusan, Pembayaran, Siswa


class ModelsTest(TestCase):
    def setUp(self):
        self.kelas = Kelas.objects.create(nama='X')
        self.jurusan = Jurusan.objects.create(nama='A')
        self.siswa = Siswa.objects.create(kelas=self.kelas, jurusan=self.jurusan, nama='namatest')
        self.pembayaran = Pembayaran.objects.create(id_siswa=self.siswa.pk,
                                    bulan_yang_dibayar=timezone.now().date(),
                                    nominal_yang_dibayar=100000,
                                    tanggal_pembayaran=timezone.now().date())

    def test_siswa_str_return(self):
        self.assertEqual(str(self.siswa), 'namatest')

    def test_pembayaran_str_return(self):
        self.assertEqual(str(self.pembayaran), "{}".format(self.siswa.pk))
