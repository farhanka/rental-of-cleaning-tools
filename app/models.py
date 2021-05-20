from djongo import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator 


class User(AbstractUser):
    hp = models.CharField(max_length=14)
    foto = models.ImageField(default="profil/default-profil",null=True, blank=True, upload_to="profil/")


    def __str__(self):
        return self.username

class Alat(models.Model):
    User = get_user_model()
    ctype = (
        ('Jam', 'Jam'),
        ('Hari', 'Hari'),
    )

    nama_alat = models.CharField(max_length=25)
    harga = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(25000000)])
    durasi = models.CharField(max_length=20, choices=ctype, default="Hari")
    keterangan = models.TextField(blank=True, max_length=255)
    tersedia = models.BooleanField(default=True)
    gambar = models.ImageField(default="img/default-alat", null=True, blank=True, upload_to="img/")
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama_alat



class Penyewaan(models.Model):
    User = get_user_model()
    durasi = models.IntegerField()
    waktu_kembali = models.DateTimeField(auto_now=False, auto_now_add=False)
    total_harga = models.IntegerField()
    alat = models.ForeignKey(Alat, on_delete=models.CASCADE)
    penyewa = models.ForeignKey(User, on_delete=models.CASCADE,related_name='penyewa')
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE,related_name='pemilik')



