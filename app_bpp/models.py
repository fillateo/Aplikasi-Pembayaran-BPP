from django.db import models


class Kelas(models.Model):
	nama = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Daftar Kelas"

	def __str__(self):
		return self.nama


class Jurusan(models.Model):
	nama = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "Daftar Jurusan"

	def __str__(self):
		return self.nama


class Siswa(models.Model):
	nama = models.CharField(max_length=100)
	kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='daftar_siswa')
	jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE, related_name='daftar_siswa')

	class Meta:
		verbose_name_plural="Daftar Siswa"

	def __str__(self):
		return self.nama


class Pembayaran(models.Model):
	id_siswa = models.IntegerField()
	bulan_yang_dibayar = models.DateField()
	nominal_yang_dibayar = models.IntegerField()
	tanggal_pembayaran = models.DateField()

	class Meta:
		verbose_name_plural = "Daftar Pembayaran"

	def __str__(self):
		return str(self.id_siswa)
