from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('doctor/', include('doctors.urls')),
    path('patient/', include('bookings.urls')),
    path('', lambda request: redirect('accounts_home'), name='home'),
]