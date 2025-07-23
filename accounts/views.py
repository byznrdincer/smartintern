from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from profiles.models import Profile, Company

# ✅ Kayıt olma (Register)
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            if user_type == 'student':
                Profile.objects.create(user=user)
            elif user_type == 'recruiter':
                Company.objects.create(user=user, name=user.username, slug=user.username.lower())

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# ✅ Giriş yapma (Login)
def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")

            if user_type == 'student':
                try:
                    profile = Profile.objects.get(user=user)
                    return redirect('profile_detail', username=user.username)
                except Profile.DoesNotExist:
                    messages.error(request, "No student profile found.")
                    logout(request)
                    return redirect('login')

            elif user_type == 'company':
                try:
                    company = Company.objects.get(user=user)
                    return redirect('company_profile', slug=company.slug)
                except Company.DoesNotExist:
                    messages.error(request, "No company profile found.")
                    logout(request)
                    return redirect('login')

            else:
                messages.error(request, "Invalid user type selected.")
                logout(request)
                return redirect('login')

        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


# ✅ Çıkış yapma (Logout)
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
