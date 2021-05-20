from django.shortcuts import render, redirect
from app.models import Alat, Penyewaan, User
from app.forms import *
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model 
from datetime import timedelta  , datetime
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.db.models import Q
import pytz


class MyLoginView(LoginView):

    form_class = LoginForm
    template_name = 'registration/login.html'


@login_required(login_url=settings.LOGIN_URL)
def profil(request):
    args = {}
    user = request.user
    if request.POST:
        form = FormEditProfil(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Berhasil memperbarui akun")
            return redirect('profil')
        else:
            args['form'] = form
            messages.error(request, "Gagal memperbarui akun")
            return render(request,'registration/profil.html', args)
    else:
        form = FormEditProfil(instance=user)
        context = {
            'form':form
        }
        return render(request, 'registration/profil.html',context)

def landing(request):
    return render(request, 'index.html')

def is_over():
    utc=pytz.UTC
    # utc=pytz.UTC
    penyewaan = Penyewaan.objects.all()
    for p in penyewaan:
        # waktu_ambil = p.waktu_ambil
        waktu_kembali = p.waktu_kembali
        date_now = utc.localize(datetime.now())
        # waktu_kembali = utc.localize(waktu_kembali)
        # print("Ambil:",waktu_ambil)
        print("Kembali:", waktu_kembali)
        print("Sekarang:", date_now)
        if  date_now > waktu_kembali:
            alat = Alat.objects.get(id=p.alat.id)
            alat.tersedia = True
            alat.save()


   
def daftar(request):
    args = {}
    if request.POST:
        form = FormDaftar(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.foto = "profil/default.png"
            form.save()
            messages.success(request, "Berhasil membuat akun")
            return redirect('masuk')
        else:
            messages.error(request, "Gagal membuat akun, pastikan form diisi dengan benar.")
            args['form'] = form
            return render(request,'registration/daftar.html', args)
    else:
        form = FormDaftar()
        context = {
            'form':form
        }
        return render(request, 'registration/daftar.html', context)



@login_required(login_url=settings.LOGIN_URL)
def home(request):
    is_over()
    User = get_user_model()
    tools = Alat.objects.all()

    if(request.user.first_name == "" or request.user.last_name == "" or request.user.email == ""):
        messages.info(request, "Profil Anda belum lengkap")

    context = {
        'tools': tools,
        'u':User
    }

    return render(request, 'home.html', context)

@login_required(login_url=settings.LOGIN_URL)
def halaman_sewa(request, id_alat):
    User = get_user_model()
    tool = Alat.objects.get(id=id_alat)
    context = {
        'tool': tool,
    }
    return render(request, 'sewa.html', context )

@login_required(login_url=settings.LOGIN_URL)
def sewa(request, id_alat):
    tool = Alat.objects.get(id=id_alat)
    pemilik = tool.pemilik
    interval = request.POST['durasi']
    harga = tool.harga * int(interval)
    
    if(tool.durasi == "Hari"):
        interval = int(interval)*24
        
    penyewaan = Penyewaan.objects.create(
        durasi = interval,
        alat = tool,
        penyewa = request.user,
        pemilik = pemilik,
        total_harga = harga,
        waktu_kembali = datetime.now() + timedelta(hours=int(interval))
    )

    penyewaan.save()
    tool.tersedia = False
    tool.save()
    messages.success(request, "Berhasil menyewa alat")
    return redirect('home')


@login_required(login_url=settings.LOGIN_URL)
def sewakan (request):
    print(request.user.id)
    args = {}
    if request.POST:
        form = FormAlat(request.POST, request.FILES)
        if form.is_valid():
            # print(request.POST['gambar'])
            alat = form.save(commit=False)
            alat.pemilik = request.user
            alat.save()
 
            form = FormAlat()
            success = "Alat berhasil di upload"
            context = {
            'form': form,
            'pesan': success
            }
            return render(request, 'sewakan.html', context)
        else:
            args['form'] = form
            # messages.error(request, "Gagal memperbarui akun")
            return render(request,'sewakan.html', args)


    form = FormAlat()
    context = {
    'form': form,
    }
    return render(request, 'sewakan.html', context)


@login_required(login_url=settings.LOGIN_URL)
def my_item(request):
    user = request.user
    my_items =  Alat.objects.filter(pemilik_id=user.id)
    # penyewaan = Penyewaan.objects.filter(pemilik = user.id).prefetch_related('my_items')
    # print(len(penyewaan))
    context = {
        'my_items':my_items,
        # 'sewa':penyewaan
    }
    return render(request, 'myitem.html', context)

def ubah_my_item(request, id_alat):
    my_item = Alat.objects.get(id=id_alat)
    template = 'ubah-item.html'
    if request.POST:
        form = FormAlat(request.POST, request.FILES, instance=my_item)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diperbarui")
            return redirect('ubah',id_alat=id_alat)
        else:
            messages.error(request, "Data gagal diperbarui")
            return redirect('ubah',id_alat=id_alat)

    else:
        form = FormAlat(instance=my_item)
        context = {
            'form':form,
            'my_item':my_item
        }
    return render(request, template, context)


def hapus_my_item(request, id_alat):
    my_item = Alat.objects.get(id=id_alat)
    my_item.delete()
    return redirect('my')
    
@login_required(login_url=settings.LOGIN_URL)
def status_sewa(request):
    wib = pytz.timezone('Asia/Jakarta')
    penyewaan = Penyewaan.objects.filter(Q(penyewa_id=request.user.id) | Q(pemilik_id=request.user.id )).prefetch_related('alat')
    today = wib.localize(datetime.now())
    context = {
        'penyewaan':penyewaan,
        'today':today
    }
    return render(request, 'status.html', context)

@login_required(login_url=settings.LOGIN_URL)
def selesai(request, sewa_id):
    # penyewaan = Penyewaan.objects.get()
    penyewaan = Penyewaan.objects.get(id=sewa_id)
    alat = Alat.objects.get(id=penyewaan.alat.id)
    alat.tersedia = True
    alat.save()
    penyewaan.delete()
    return redirect('status')
    
def about(request):
    return render(request, 'about.html')

