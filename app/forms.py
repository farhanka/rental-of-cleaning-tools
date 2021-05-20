from django.forms import ModelForm
from django import forms
from app.models import Alat, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
# from django.contrib.auth.models import User

class FormAlat(ModelForm):
    class Meta:
        model = Alat
        fields = ['nama_alat', 'harga', 'durasi','keterangan','tersedia','gambar']


        widgets = {
            'nama_alat': forms.TextInput({'class':'form-control', 'placeholder':'Mesin Potong Rumput'}),
            'harga': forms.NumberInput({'class':'form-control', 'placeholder':'50000'}),
            'durasi': forms.Select({'class':'form-select'}),
            'keterangan': forms.Textarea({'class':'form-control','placeholder':'Sudah termasuk bensin'}),
            'gambar': forms.FileInput({'class':'form-control'})
            }
            
class FormDaftar(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Kata Sandi tidak sama."),
        'username_taken': _("Nama pengguna sudah digunakan.")
  
    }
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}), label="Kata Sandi"
        )

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control'}), label="Konfirmasi Kata Sandi"
        # help_text="Minimal 8 karakter gabungan angka dan huruf"
        )
        

 
    class Meta:
        model = User
        fields = ['username','hp','password1', 'password2']
        help_texts = {
            'username': 'Hanya huruf, angka, dan @/./+/-/_',
        }

        widgets = {
            'username': forms.TextInput({'class':'form-control'}),
            'hp': forms.NumberInput({'class':'form-control'}),
        }
        
        
class FormEditProfil(UserChangeForm):
    foto = forms.ImageField()
    hp = forms.CharField(max_length=14)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name','hp','email','foto']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.PasswordInput(
    attrs={'class':'form-control','type':'text', 'name': 'username'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password'}),
        label="Kata Sandi"
        )
