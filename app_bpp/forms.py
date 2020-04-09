from django import forms
from .models import *


class SiswaForm(forms.ModelForm):
    class Meta:
        model = Siswa
        fields = '__all__'

        widgets = {
        	'nama': forms.TextInput(
        			attrs={
        				'class': 'form-control basic-ele-mg-b-10 responsive-mg-b-10',
        				'placeholder': 'Nama lengkap',
        			}
        		),
        	'kelas': forms.Select(
        			attrs={
        				'class': 'form-control custom-select-value',
        			}
        		),
        	'jurusan': forms.Select(
        			attrs={
        				'class': 'form-control custom-select-value',
        			}
        		)
        }


 
class PembayaranForm(forms.ModelForm):
    class Meta:
        model = Pembayaran
        fields = '__all__'


class KelasForm(forms.ModelForm):
    class Meta:
        model = Kelas
        fields = '__all__'

        widgets = {
            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control basic-ele-mg-b-10 responsive-mg-b-10',
                    'placeholder': 'Kelas',
                }
                )
        }


class JurusanForm(forms.ModelForm):
    class Meta:
        model = Jurusan
        fields = '__all__'

        widgets = {
            'nama': forms.TextInput(
                attrs={
                    'class': 'form-control basic-ele-mg-b-10 responsive-mg-b-10',
                    'placeholder': 'Jurusan',
                }
                )
        }