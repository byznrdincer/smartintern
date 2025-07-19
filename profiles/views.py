from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    # Kullanıcının profil bilgilerini template’e gönder
    return render(request, 'profiles/profile_detail.html', {'profile_user': user})

def profile_edit(request, username):
    # Profil düzenleme işlemleri burada olacak
    return render(request, 'profiles/profile_edit.html')
