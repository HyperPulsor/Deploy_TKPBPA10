from datetime import datetime
from django.shortcuts import render,redirect
from forum.models import ForumUMKM, Replies
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required,permission_required
from account.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

def show_json_flutter(request):
    data = ForumUMKM.objects.all().order_by('-time')
    print(data)
    return HttpResponse(serializers.serialize("json", data))

def show_json_reply_flutter(request,forum_id):
    this_forum = ForumUMKM.objects.filter(id=forum_id).first()
    data = Replies.objects.filter(forum=this_forum)
    return HttpResponse(serializers.serialize("json", data))

@login_required(login_url='/account/login/')
def show_json(request,kategori_inputuser):
    if kategori_inputuser == "semua":
        data = ForumUMKM.objects.all().order_by('-time')
        return HttpResponse(serializers.serialize("json", data))

    data = ForumUMKM.objects.filter(kategori=kategori_inputuser).order_by('-time')
    return HttpResponse(serializers.serialize("json", data))

def main(request,kategori_inputuser):
    data = ""
    category_list = ["semua","makanan","pakaian","perlengkapan rumah tangga", "otomotif", "alat tulis kantor", "kesehatan", "kecantikan","musik", "gadget", "aksesoris", "footwear", "tas"]
   
    if kategori_inputuser == "semua":
        data = ForumUMKM.objects.all()
        content={'data':data, 'list_category':category_list,'selected_cat':"semua"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "makanan":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"makanan"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "pakaian":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"pakaian"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "perlengkapan":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"perlengkapan"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "otomotif":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"otomotif"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "alat":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"alat"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "kesehatan":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"kesehatan"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "kecantikan":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"kecantikan"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "musik":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"musik"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "gadget":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"gadget"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "aksesoris":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"aksesoris"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "footwear":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"footwear"}
        return render(request, "front.html", content)

    elif kategori_inputuser == "tas":
        data = ForumUMKM.objects.filter(kategori=kategori_inputuser)
        content={'data':data, 'list_category':category_list,'selected_cat':"tas"}
        return render(request, "front.html", content)

def show_reply(request, forum_id):
    forum = ForumUMKM.objects.filter(id=forum_id).first()
    reply = Replies.objects.filter(forum=forum)
    forum_author = (forum.user==request.user)
    #print(forum_author)
    content = {'forum': forum, 'reply':reply, 'admin':request.user.is_admin, 'buyer':request.user.is_buyer, 'seller': request.user.is_seller, 'user_forum':forum_author}
    #, 'admin':User.is_admin, 'buyer':User.is_buyer, 'seller': User.is_seller, 'user':forum.user
    return render(request, "discuss.html", content)

def show_json_reply(request,forum_id):
    this_forum = ForumUMKM.objects.filter(id=forum_id).first()
    data = Replies.objects.filter(forum=this_forum)
    return HttpResponse(serializers.serialize("json", data))

#@login_required(login_url='/account/login/')
def add_forum(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        discussion = request.POST.get('message')
        category = request.POST.get('category')
        #inget ubah user-nya
        print(user.username)
        forum = ForumUMKM(user=user,title=title,discussion=discussion,kategori=category,username=user.username)
        forum.save()
        return redirect('/forum/semua')
    return HttpResponseNotFound()

#processing penambahan forum
@csrf_exempt
def add_forum_flutter(request, id):
    if request.method == 'POST':
        newForum = json.loads(request.body)

        title=newForum['title']
        discussion = newForum['discussion']
        user = User.objects.get(id=newForum['id'])
        username = user.username
        kategori = "semua"

        newForum = ForumUMKM(title=title, discussion=discussion, user=user, kategori=kategori, username = username)
        newForum.save();
        return JsonResponse({"instance": "Forum Berhasil Dibuat!"}, status=200)


@csrf_exempt
def add_reply_flutter(request, id):
    if request.method == 'POST':
        newReply = json.loads(request.body)

        discussion = newReply['discussion']
        user = User.objects.get(id=newReply['id'])
        username = user.username
        forum = ForumUMKM.objects.get(id=newReply['forum_pk'])
        #cara akses forum?

        newReply = Replies(discussion=discussion, user=user, username = username,forum=forum)
        newReply.save();
        return JsonResponse({"instance": "Reply Berhasil Dibuat!"}, status=200)

def add_reply(request):
    if request.method == "POST":
        print(request.POST)
        user = request.user
        discussion = request.POST.get('message')
        forum = int(request.POST.get('repforum'))
        #inget ubah user-nya jadi user=user
        this_forum = ForumUMKM.objects.filter(id=forum).first()
        reply = Replies(user=user, discussion=discussion,forum=this_forum,username=user.username)
        reply.save()
        return redirect('/forum/discussion/{}'.format(forum))
    return HttpResponseNotFound()

#admin only
#@login_required(login_url='/account/login/')
def delete_forum(request, forum_id):
    forum = ForumUMKM.objects.get(pk=forum_id)
    forum.delete()
    forum = ForumUMKM.objects.all()
    return HttpResponseRedirect('/forum/semua')