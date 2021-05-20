from django.contrib import admin
from app.models import Alat, Penyewaan
from django.contrib.auth import get_user_model

class AlatAdmin(admin.ModelAdmin):
    list_display = ['nama_alat','harga', 'keterangan','gambar']

class UserAdmin(admin.ModelAdmin):
    # list_display = ['nama','hp']
    list_display = ['username','hp']

class PenyewaanAdmin(admin.ModelAdmin):
    list_display = ['alat_id', 'penyewa_id']

# Register your models here.
admin.site.register(Alat, AlatAdmin)
admin.site.register(Penyewaan, PenyewaanAdmin)
admin.site.register(get_user_model(), UserAdmin)

