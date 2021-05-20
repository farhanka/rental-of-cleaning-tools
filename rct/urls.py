from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('home/', home, name='home'),
    path('sewakan/',sewakan, name='sewakan'),
    path('status/', status_sewa, name='status'),
    path('my/', my_item, name='my'),
    path('masuk/', MyLoginView.as_view(), name='masuk'),
    path('keluar/', LogoutView.as_view(next_page='masuk'),name='keluar'),
    path('daftar/', daftar, name='daftar'),
    path('my/ubah/<int:id_alat>', ubah_my_item, name="ubah"),
    path('my/hapus/<int:id_alat>', hapus_my_item, name="hapus"),
    path('sewa/<int:id_alat>', halaman_sewa, name="halaman_sewa"),
    path('alat/<int:id_alat>/', sewa, name="sewa"),
    path('status/', status_sewa, name='status'),
    path('selesai/<int:sewa_id>', selesai, name='selesai'),
    path('profil/', profil, name='profil'),
    path('about/', about, name='about'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

