import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from addkategori.models import Kategori

# import form
from .forms import FormKategori
# import dll
from django.shortcuts import redirect
# import buat pict
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

# Create your views here.

def show_kategori(request):
    form = FormKategori()
    data = Kategori.objects.all()
    context = {
        'title' : 'Kategori Product',
        'list_kategori' : data,
        'form' : form,
        }
    return render(request, "main.html", context)

# @csrf_exempt
def create_kategori(request):
    if request.method == "POST":
        user = request.user
        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        gambar = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(gambar.name, gambar)
        file_url = fss.url(file)
        if nama != "" and deskripsi != "":
            Kategori.objects.create(deskripsi=deskripsi, nama=nama, gambar=gambar, file_url=file_url)
            return redirect('kategori:show_kategori')
        else:
            list(messages.get_messages(request))
            messages.error(request, "Nama dan Deskripsi Kategori Harus Diisi")
    return render(request, 'create_kategori.html')

@csrf_exempt
def create_kategori_flutter(request):
    if request.method == 'POST':
        newKategori = json.loads(request.body)

        nama = newKategori['nama']
        deskripsi = newKategori['deskripsi']
        file_url = newKategori['file_url']

        newKategori = Kategori(nama=nama, deskripsi=deskripsi, file_url=file_url)
        newKategori.save();
        return JsonResponse({"instance": "Kategori Berhasil Dibuat!"}, status=200)
        
def delete_kategori(request, id):
    deletekategori = Kategori.objects.get(pk=id)
    deletekategori.delete()
    return redirect('kategori:show_kategori')

def show_json(request):
    data = Kategori.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")