from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import *


############## Siswa & Pembayaran ##############

# convert string (rupiah) to integer format
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

	return render(request, 'app_bpp/form_siswa.html', {'form': form, 'header': 'Tambah siswa'})

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
		request.POST['bulan_yang_dibayar'] = "{}/{}".format(1, request.POST['bulan_yang_dibayar']) # set to 1/mm/YYYY
		request.POST['bulan_yang_dibayar'] = change_date_format(request.POST['bulan_yang_dibayar'])
		request.POST['tanggal_pembayaran'] = change_date_format(request.POST['tanggal_pembayaran'])

		if form.is_valid():
			form.save()
			return redirect(reverse('app_bpp:detail_siswa', kwargs={'pk': pk}))

	context = {
		'siswa': siswa,
		'current_date': timezone.now().date().strftime("%d/%m/%Y"),
		'form': form,
		'riwayat_pembayaran': riwayat_pembayaran,
	}

	return render(request, 'app_bpp/detail_pembayaran_siswa.html', context)

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
	# else:
	# 	return HttpResponse('Invalid!')

	context = {
		'siswa': siswa,
		'form': form,
		'header': 'Ubah siswa',
	}
	return render(request, 'app_bpp/form_siswa.html', context)

@login_required
def hapus_siswa_view(request, pk):
	get_object_or_404(Siswa, pk=pk).delete()
	pembayaran = Pembayaran.objects.filter(id_siswa=pk)

	if len(pembayaran) > 0:
		pembayaran.delete()

	return redirect('app_bpp:daftar_siswa')

@login_required
def ubah_riwayat_pembayaran_view(request, id_siswa, pk):
	riwayat_pembayaran = get_object_or_404(Pembayaran, id_siswa=id_siswa, pk=pk)
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
			return redirect(reverse('app_bpp:detail_siswa', kwargs={'pk': siswa.id}))

	context = {
		'riwayat_pembayaran': riwayat_pembayaran,
		'siswa': siswa,
		'form': form,
	}

	return render(request, 'app_bpp/form_riwayat_pembayaran.html', context)

@login_required
def hapus_riwayat_pembayaran_view(request, id_siswa, pk):
	get_object_or_404(Pembayaran, id_siswa=id_siswa, pk=pk).delete()
	return redirect(reverse('app_bpp:detail_siswa', kwargs={'pk': id_siswa}))

############## End Siswa & Pembayaran ##############

############## Kelas ##############

@login_required
def tambah_kelas_view(request):
	form = KelasForm(request.POST)

	if form.is_valid():
		form.save()
		return redirect('app_bpp:daftar_kelas')
	return render(request, 'app_bpp/form_kelas.html', {'form': form})

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
		return redirect('/ubah_kelas/{}/'.format(pk))
	else:
		if request.method == "POST":
			messages.error(request, 'Gagal!')

	return render(request, 'app_bpp/form_kelas.html', {'form': form, 'header': 'Ubah kelas'})

@login_required
def hapus_kelas_view(request, pk):

	# remove daftar pembayaran for siswa FOR current kelas
	for siswa in Siswa.objects.filter(kelas=pk):
		if Pembayaran.objects.exists():
			Pembayaran.objects.filter(id_siswa=siswa.pk).delete()

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
	else:
		from django.http import HttpResponse
		return HttpResponse('Invalid data!')

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
		return redirect('app_bpp:daftar_jurusan')

	else:
		if request.method == "POST":
			messages.error(request, 'Gagal!')

	return render(request, 'app_bpp/form_jurusan.html', {'form': form, 'header': 'Ubah jurusan'})

@login_required
def hapus_jurusan_view(request, pk):

	# remove daftar pembayaran for siswa FOR current jurusan
	for siswa in Siswa.objects.filter(jurusan=pk):
		if Pembayaran.objects.exists():
			Pembayaran.objects.filter(id_siswa=siswa.pk).delete()

	get_object_or_404(Jurusan, pk=pk).delete()
	return redirect('app_bpp:daftar_jurusan')

############## End Jurusan ##############

############## Chart ##############

def get_gte_yang_melakukan_pembayaran():
	current_month = int(timezone.now().date().strftime("%m"))
	current_year = int(timezone.now().date().strftime("%Y"))
	pembayaran_bulan_ini_lebih = Pembayaran.objects.filter(bulan_yang_dibayar__gte=datetime.date(current_year, current_month, 1))
	jumlah_siswa_yang_membayar_bulan_ini_lebih = pembayaran_bulan_ini_lebih.values("id_siswa").distinct()
	return jumlah_siswa_yang_membayar_bulan_ini_lebih

def get_le_yang_melakukan_pembayaan():
	jumlah_siswa = len(Siswa.objects.all())
	return jumlah_siswa - len(get_gte_yang_melakukan_pembayaran())

# def lunas_hingga_bulan_ini_per_jurusan():
# 	data = dict()
#
# 	for jurusan in Jurusan.objects.values_list("nama", flat=True):
# 		data[jurusan] = 0
#
# 	for siswa in get_gte_yang_melakukan_pembayaran():
# 		jurusan = Siswa.objects.get(pk=siswa['id_siswa']).jurusan
#
# 		if str(jurusan) in data.keys():
# 			data[str(jurusan)] += 1
#
# 	return data

@login_required
def chart_view(request):
	list_siswa = Siswa.objects.all()
	list_kelas = list(set([siswa.kelas for siswa in list_siswa]))
	context = {
		'jumlah_siswa_yang_membayar_bulan_ini_lebih': len(get_gte_yang_melakukan_pembayaran()),
		'jumlah_siswa_yang_tdk_membayar_bulan_ini_lebih': get_le_yang_melakukan_pembayaan(),
		'list_kelas': list_kelas,
		'jumlah_siswa': len(list_siswa),
		# 'lunas_bulan_ini': lunas_hingga_bulan_ini_per_jurusan(),
	}

	return render(request, 'app_bpp/chart.html', context)

############## End Chart ##############
