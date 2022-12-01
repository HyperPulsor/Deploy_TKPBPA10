from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import SignUpBuyerForm, SignUpSellerForm, LoginForm, DonasiForm
from django.contrib.auth import authenticate, login, logout
import json
from addkategori.models import Kategori
from adminfaq.models import Faq
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

# Create your views here.

def donasi_barang(request):
    form = DonasiForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        barang = form.cleaned_data['input_barang']
        Donasi.objects.create(user=request.user, tipe=True, input_uang=0, input_barang=barang)
    return render (request, 'donasi.html')

def index(request):
    return render(request, 'index.html')

def registerbuyer(request):
    msg = None
    if request.method == 'POST':
        form = SignUpBuyerForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('account:login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpBuyerForm()
    return render(request,'registerbuyer.html', {'form': form, 'msg': msg})

def registerseller(request):
    msg = None
    if request.method == 'POST':
        form = SignUpSellerForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('account:login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpSellerForm()
    return render(request,'registerseller.html', {'form': form, 'msg': msg})

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('account:adminpage')
            elif user is not None and user.is_buyer:
                login(request, user)
                return redirect('account:buyer')
            elif user is not None and user.is_seller:
                login(request, user)
                return redirect('account:seller')
            else:
                msg= 'Akun tidak ditemukan'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def admin(request):
    kategori_item = Kategori.objects.all()
    context = {
        'kategori_item' : kategori_item,
    }
    return render(request,'show_admin.html', context)

def buyer(request):
    kategori_item = Kategori.objects.all()
    context = {
        'kategori_item' : kategori_item,
    }
    return render(request,'show_pembeli.html', context)

def seller(request):
    kategori_item = Kategori.objects.all()
    context = {
        'kategori_item' : kategori_item,
    }
    return render(request,'show_penjual.html', context)

def logout_user(request):
    logout(request)
    return redirect('account:index')

def show_json(request):
    data = Kategori.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def login_flutter(request):
	context = {}
	user = request.user
	
	if request.method == "POST":
		data = json.loads(request.body)
		email = data['email']
		password = data['password']
		user = authenticate(request, email=email, password=password)
		if user:
			login(request, user)
			context['login'] = "logged-in"
			context['user'] = {"email": user.email, "username": user.username}
			return JsonResponse({'data': context}, status=200)

	context['login'] = 'unlogin'
	return JsonResponse({'data': context}, status=500)


@csrf_exempt
def signup_flutter(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		email = data['email']
		username = data['username']
		password = data['password']
		
		try:
			new_user = User.objects.create_user(email, username, password)
			new_user.save()
			return JsonResponse({"instance": "user Dibuat"}, status=200)
		except:
			return JsonResponse({"instance": "gagal Dibuat"}, status=400)

	return JsonResponse({"instance": "gagal Dibuat"}, status=400)

@csrf_exempt
def logout_flutter(request):
	data = json.loads(request.body)
	if request.user.is_authenticated or data['loggedIn']:
		if request.user.is_authenticated:
			logout(request)
		return JsonResponse({"status" : "loggedout"}, status=200)
	return JsonResponse({"status": "Not yet authenticated"}, status =403)

@csrf_exempt
def get_user(request):
	user = request.user
	if not user.is_authenticated:
		return JsonResponse({"result": "Not yet authenticated!"}, status=403)
	
	user = User.objects.get(username=user)
	return JsonResponse({"data": {"email": user.email, "username": user.username}}, status=200)
