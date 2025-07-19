from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),  # /profile/beyzanur/
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),  # Profil düzenleme (opsiyonel)
]
