from django.conf.urls import url
from .views import *


app_name = "app_bpp"

urlpatterns = [
	url(r'^daftar_kelas/$', list_kelas_view, name="daftar_kelas"),
	url(r'^tambah_kelas/$', tambah_kelas_view, name="tambah_kelas"),
	url(r'^ubah_kelas/(?P<pk>\d+)/$', ubah_kelas_view, name="ubah_kelas"),
	url(r'^hapus_kelas/(?P<pk>\d+)/$', hapus_kelas_view, name="hapus_kelas"),

	url(r'^daftar_jurusan/$', list_jurusan_view, name="daftar_jurusan"),
	url(r'^tambah_jurusan/$', tambah_jurusan_view, name="tambah_jurusan"),
	url(r'^ubah_jurusan/(?P<pk>\d+)/$', ubah_jurusan_view, name="ubah_jurusan"),
	url(r'^hapus_jurusan/(?P<pk>\d+)/$', hapus_jurusan_view, name="hapus_jurusan"),

	url(r'^hapus_siswa/(?P<pk>\d+)/$', hapus_siswa_view, name="hapus_siswa"),
	url(r'^ubah_siswa/(?P<pk>\d+)/$', ubah_siswa_view, name="ubah_siswa"),
	url(r'^daftar_siswa/$', list_siswa_view, name="daftar_siswa"),
	url(r'^tambah_siswa/$', tambah_siswa_view, name="tambah_siswa"),
	url(r'^detail_siswa/(?P<pk>\d+)/$', detail_siswa_dan_pembayaran_view, name="detail_siswa"),
	url(r'^$', home_view, name="home"),

	url(r'^ubah_riwayat_pembayaran/(?P<id_siswa>\d+)/(?P<pk>\d+)/$', ubah_riwayat_pembayaran_view, name="ubah_riwayat_pembayaran"),
	url(r'^hapus_riwayat_pembayaran/(?P<id_siswa>\d+)/(?P<pk>\d+)/$', hapus_riwayat_pembayaran_view, name="hapus_riwayat_pembayaran"),

	url(r'^chart/$', chart_view, name="chart"),
]