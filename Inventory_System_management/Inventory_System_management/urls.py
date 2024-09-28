from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),  # Authentication URLs
    path('api/inventron/', include('inventron.urls')),  # CRUD app URLs
]


