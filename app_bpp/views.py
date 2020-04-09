from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import *


############## Siswa & Pembayaran ##############

# convert rupiah to integer
def rupiah_to_integer(string):
	return int(string.replace('Rp. ', '').replace(',00', '').replace('.', ''))

def change_date_format(date):
	date = date.split("/")
	date = "{}/{}/{}".format(date[1], date[0], date[2])
	return date

@login_required
def tambah_siswa_view(request):
	form = SiswaForm(request.POST or None)

	if form.is_valid():
		form.save()
		messages.success(request, "\"{}\" berhasil ditambahkan!".format(request.POST['nama']))
		return redirect('app_bpp:tambah_siswa')
	else:
		if request.POST:
			messages.error(request, "Gagal menambahkan data!")

	return render(request, 'app_bpp/form.html', {'form': form, 'header': 'Tambah siswa'})

@login_required
def home_view(request):
	daftar_siswa = Siswa.objects.all().order_by('jurusan')
	return render(request, 'app_bpp/index.html', {'daftar_siswa': daftar_siswa})

@login_required
def detail_siswa_dan_pembayaran_view(request, pk):
	siswa = get_object_or_404(Siswa, pk=pk)
	form = PembayaranForm(request.POST or None)
	riwayat_pembayaran = Pembayaran.objects.filter(id_siswa=pk).order_by('-id')

	if request.method == 'POST':

		if not request.POST._mutable:
			request.POST._mutable = True

		request.POST['nominal_yang_dibayar'] = rupiah_to_integer(request.POST['nominal_yang_dibayar'])
		request.POST['id_siswa'] = pk
		request.POST['bulan_yang_dibayar'] = "{}/{}".format(1, request.POST['bulan_yang_dibayar'])
		request.POST['bulan_yang_dibayar'] = change_date_format(request.POST['bulan_yang_dibayar'])
		request.POST['tanggal_pembayaran'] = change_date_format(request.POST['tanggal_pembayaran'])

		if form.is_valid():
			form.save()

	context = {
		'siswa': siswa, 
		# 'current_date': timezone.now(), 
		'form': form,
		'riwayat_pembayaran': riwayat_pembayaran,
	}
	return render(request, 'app_bpp/detail.html', context)

@login_required
def list_siswa_view(request):
	daftar_siswa = Siswa.objects.all().order_by('jurusan')
	context = {
		'daftar_siswa': daftar_siswa,
	}
	return render(request, 'app_bpp/list_siswa.html', context)

@login_required
def ubah_siswa_view(request, pk):
	siswa = get_object_or_404(Siswa, pk=pk)
	form = SiswaForm(request.POST or None, instance=siswa)

	if form.is_valid():
		form.save()
		messages.success(request, 'Siswa telah dirubah!')
		return redirect('/ubah_siswa/{}/'.format(pk))	

	context = {
		'siswa': siswa,
		'form': form,
		'header': 'Ubah siswa',
	}
	return render(request, 'app_bpp/form.html', context)

@login_required
def hapus_siswa_view(request, pk):
	get_object_or_404(Siswa, pk=pk).delete()
	get_object_or_404(Pembayaran, id_siswa=pk).delete()
	return redirect('app_bpp:daftar_siswa')

@login_required
def ubah_riwayat_pembayaran_view(request, id_siswa, pk):
	riwayat_pembayaran = Pembayaran.objects.get(id_siswa=id_siswa, pk=pk)
	siswa = Siswa.objects.get(pk=riwayat_pembayaran.id_siswa)
	form = PembayaranForm(request.POST or None, instance=riwayat_pembayaran)

	if request.method == 'POST':

		if not request.POST._mutable:
			request.POST._mutable = True

		request.POST['nominal_yang_dibayar'] = rupiah_to_integer(request.POST['nominal_yang_dibayar'])
		request.POST['id_siswa'] = id_siswa
		request.POST['bulan_yang_dibayar'] = "{}/{}".format(1, request.POST['bulan_yang_dibayar'])
		request.POST['bulan_yang_dibayar'] = change_date_format(request.POST['bulan_yang_dibayar'])
		request.POST['tanggal_pembayaran'] = change_date_format(request.POST['tanggal_pembayaran'])

		if form.is_valid():
			form.save()
			return redirect('/detail_siswa/{}/'.format(siswa.id))

	context = {
		'riwayat_pembayaran': riwayat_pembayaran,
		'siswa': siswa,
		'form': form,
	}

	return render(request, 'app_bpp/form_riwayat_pembayaran.html', context)

@login_required
def hapus_riwayat_pembayaran_view(request, id_siswa, pk):
	get_object_or_404(Pembayaran, id_siswa=id_siswa, pk=pk).delete()
	return redirect('/detail_siswa/{}'.format(id_siswa))

############## End Siswa & Pembayaran ##############

############## Kelas ##############

@login_required
def tambah_kelas_view(request):
	form = KelasForm(request.POST)

	if form.is_valid():
		form.save()
		return redirect('app_bpp:daftar_kelas')

@login_required
def list_kelas_view(request):
	daftar_kelas = Kelas.objects.all()
	form = KelasForm()
	context = {
		'daftar_kelas': daftar_kelas,
		'form': form,
	}
	return render(request, 'app_bpp/list_kelas.html', context)

@login_required
def ubah_kelas_view(request, pk):
	kelas = get_object_or_404(Kelas, pk=pk)
	form = KelasForm(request.POST or None, instance=kelas)

	if form.is_valid():
		form.save()
		messages.success(request, 'Berhasil!')
	else:
		if request.method == "POST":
			messages.error(request, 'Gagal!')

	return render(request, 'app_bpp/form_kelas.html', {'form': form, 'header': 'Ubah kelas'})

@login_required
def hapus_kelas_view(request, pk):
	get_object_or_404(Kelas, pk=pk).delete()
	return redirect('app_bpp:daftar_kelas')

############## End Kelas ##############

############## Jurusan ##############

@login_required
def tambah_jurusan_view(request):
	form = JurusanForm(request.POST)

	if form.is_valid():
		form.save()
		messages.success(request, request.POST['nama'])
		return redirect('app_bpp:daftar_jurusan')

@login_required
def list_jurusan_view(request):
	daftar_jurusan = Jurusan.objects.all()
	form = JurusanForm()
	context = {
		'daftar_jurusan': daftar_jurusan,
		'form': form,
	}
	return render(request, 'app_bpp/list_jurusan.html', context)

@login_required
def ubah_jurusan_view(request, pk):
	jurusan = get_object_or_404(Jurusan, pk=pk)
	form = JurusanForm(request.POST or None, instance=jurusan)

	if form.is_valid():
		form.save()
		messages.success(request, 'Berhasil!')
	else:
		if request.method == "POST":
			messages.error(request, 'Gagal!')

	return render(request, 'app_bpp/form_jurusan.html', {'form': form, 'header': 'Ubah jurusan'})

@login_required
def hapus_jurusan_view(request, pk):
	get_object_or_404(Jurusan, pk=pk).delete()
	return redirect('app_bpp:daftar_jurusan')

############## End Jurusan ##############