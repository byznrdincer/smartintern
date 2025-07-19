

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),          
    path('accounts/', include('accounts.urls')),  
    path('profiles/', include('profiles.urls')),  
    path('projects/', include('projects.urls')),  
    
]

