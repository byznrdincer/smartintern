from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),  # Öğrenci profili
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),  # Profil düzenleme (opsiyonel)
    path('company/<slug:slug>/', views.company_profile, name='company_profile'),  # Şirket profili
]
