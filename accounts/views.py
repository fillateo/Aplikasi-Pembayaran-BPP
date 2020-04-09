from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash


def login_view(request):	

	if request.user.is_authenticated():
		return redirect('app_bpp:home')

	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		
		if form.is_valid():
			user = form.get_user()
			login(request, user)

			return redirect('app_bpp:home')
		else:
			messages.error(request, "Nama pengguna/Kata sandi salah!")

	else:
		form = AuthenticationForm()

	return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('accounts:login')