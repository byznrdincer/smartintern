from django.urls import path
from . import views

urlpatterns = [
    path('profile/redirect/', views.profile_redirect, name='profile_redirect'),
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('company/<slug:slug>/', views.company_profile, name='company_profile'),
]
