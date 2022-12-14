import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from account.forms import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

@login_required(login_url='/account/login/')
def show_profile(request):
    if not request.user.is_authenticated:
        return redirect("account/login/")
    if request.user is not None and request.user.is_buyer:
                return redirect('showbuyer/')
    elif request.user is not None and request.user.is_seller:
                return redirect('showseller/')

def show_buyer(request):
    return render(request,'buyer-profile.html')

def show_seller(request):
    return render(request,'seller-profile.html')

class BuyerEditView(generic.UpdateView):
    form_class = BuyerEditProfileForm
    template_name = 'buyer-profile-edit.html'
    success_url = reverse_lazy('profile:showbuyer')

    def get_object(self):
        return self.request.user

class SellerEditView(generic.UpdateView):
    form_class = SellerEditProfileForm
    template_name = 'seller-profile-edit.html'
    success_url = reverse_lazy('profile:showseller')

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('profile:password_success')

def password_success(request):
    return render(request, 'password-success.html', {})

# @csrf_exempt
# def edit_profile(request, id):
#     if request.method == 'POST':
#         newForum = json.loads(request.body)

#         username=request.username
#         email=request.email

#         newForum = User(username=username, email=email)
#         newForum.save();
#         return JsonResponse({"instance":"Berhasil memperbarui data"}, status=200)

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']  
        email = data['email']  

        if username and email:
            user = User.objects.get(username = username)
            u_form = BuyerEditProfileForm(request.POST or None, instance=user)
            # p_form = ProfileUpdateForm(request.POST or None,
            #                             request.FILES or None,
            #                             instance=profile)
            tmp_uform = u_form.save(commit = False)
            # tmp_pform = p_form.save(commit = False)

            tmp_uform.username = username
            tmp_uform.email = email
            # tmp_pform.bio = bio

            # tmp_pform.save()
            tmp_uform.save()

            response = {
                'msg':  'Update profil Anda berhasil disimpan!',
                'id' : 1,
                'status': 'success'
            }
        return JsonResponse(response)
    else:
        return JsonResponse({"status": "error"})