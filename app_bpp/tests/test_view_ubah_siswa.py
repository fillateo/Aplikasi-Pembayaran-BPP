from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ..models import Siswa, Pembayaran, Kelas, Jurusan
from ..views import ubah_siswa_view
