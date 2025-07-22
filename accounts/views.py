from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm  # kendi formunu kullan
from profiles.models import Profile, Company
# Modellerini import et (model isimlerin tam uymalı)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Kayıt sonrası login yapılmaz
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # login sayfasına yönlendir
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")

            # Kullanıcıya ait Profile varsa öğrenci profiline yönlendir
            try:
                profile = Profile.objects.get(user=user)
                return redirect('profile_detail', username=user.username)
            except Profile.DoesNotExist:
                pass

            # Kullanıcıya ait Company varsa şirket profiline yönlendir
            try:
                company = Company.objects.get(user=user)
                return redirect('company_profile', slug=company.slug)
            except Company.DoesNotExist:
                pass

          
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
