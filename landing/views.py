from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from addkategori.models import Kategori
from django.http import HttpResponse
from django.core import serializers

@login_required(login_url='/index/')
def show_landing(request):
    kategori_item = Kategori.objects.all()
    context = {
        'kategori_item' : kategori_item,
    }
    return render(request, "show.html", context)

def show_json(request):
    data = Kategori.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")