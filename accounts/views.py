from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from profiles.models import Profile, Company
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')  # Giriş yaptıktan sonra yönlendirme
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            email_or_username = form.cleaned_data.get('username')  # Formdaki input name username, ama email gelebilir
            password = form.cleaned_data.get('password')

            # Email ile kullanıcıyı bulmaya çalış
            try:
                user_obj = User.objects.get(email=email_or_username)
                username = user_obj.username
            except User.DoesNotExist:
                username = email_or_username  # Direkt username olarak devam et

            user = authenticate(request, username=username, password=password)

            if user is not None:
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
                messages.error(request, "Authentication failed.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
