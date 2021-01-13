from django.shortcuts import render,redirect
from .forms import KeijibanForm,ProfileForm,CreateForm,CommentForm,SendMessageForm
from django.contrib.auth import authenticate, login, logout
from .models import Keijiban,Profile,Comment,Message
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# from accounts.models import CustomUser
#追加
from django.template.loader import render_to_string
from django.http import JsonResponse




def listfunc(request,now_page=1):
    object_list=Keijiban.objects.all().order_by("created_at").reverse()
    comment_list=Comment.objects.all().order_by("created_at").reverse()
    print(request.user)

    # author_list=Keijiban.objects.all().values("authorid_id").reverse()
    author_list=Keijiban.objects.all().order_by("created_at").reverse().values("authorid_id")
    profile_list=[]
    for author in author_list :
        num=author["authorid_id"]
        profile_list.append(Profile.objects.get(profileid_id=num))


    new_object_list=[]
    for i in range(len(object_list)):
        new_object=model_to_dict(object_list[i])
        new_object["username"]=profile_list[i].username
        new_object["icon"]=profile_list[i].icon
        new_object_list.append(new_object)

    page=Paginator(new_object_list,30)

    return render(request,"list.html",{"object_list":page.get_page(now_page),"comment_list":comment_list})

@login_required
def createfunc(request):
    if request.method == "POST":
        form = Keijiban.objects.create(toukou=request.POST["toukou"],image=request.FILES.get("image"),authorid_id=request.user.id)
        return redirect("list")

    else:
        createform = CreateForm()
        return render(request,"create.html",{"createform":createform})

def profilefunc(request):
    if request.method == "POST":
        form = Profile.objects.create(username=request.POST["username"],age=request.POST["age"],sex=request.POST["sex"],address=request.POST["address"],icon=request.FILES.get("icon"),profileid_id=request.user.id)
        return redirect("list")

    else:
        try:
            Profile.objects.get(profileid_id=request.user.id)
            return redirect("list")

        except:
            profileform = ProfileForm()
            return render(request,"profile.html",{"profileform":profileform})



def profiledetailfunc(request,pk):
    profile_detail=Profile.objects.get(profileid_id=pk)
    return render(request,"detail.html",{"profile_detail":profile_detail})

def profileupdatefunc(request):
    obj=Profile.objects.get(profileid_id=request.user.id)
    if request.method == "POST":
        profile_update=ProfileForm(request.POST,request.FILES,instance=obj)
        profile_update.save()
        return redirect("list")

    else:
        profile_update=ProfileForm(instance=obj)
        return render(request,"profileupdate.html",{"profile_update":profile_update,"obj":obj})


def keijibanupdatefunc(request,pk):
    obj=Keijiban.objects.get(id=pk)
    if request.method == "POST":
        keijiban_update=CreateForm(request.POST,request.FILES,instance=obj)
        keijiban_update.save()
        return redirect("list")

    else:
        keijiban_update=CreateForm(instance=obj)
        return render(request,"keijibanupdate.html",{"keijiban_update":keijiban_update,"obj":obj})


def keijibandeletefunc(request,pk):
    obj=Keijiban.objects.get(id=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("list")

    else:
        keijiban_delete=KeijibanForm(instance=obj)
        return render(request,"keijibandelete.html",{"keijiban_delete":keijiban_delete,"obj":obj})

def goodfunc(request,pk):
    keijiban=Keijiban.objects.get(id=pk)
    keijiban.good+=1
    keijiban.save()
    return redirect("list")





def commentcreatefunc(request,pk):
    profile=Profile.objects.get(profileid_id=request.user.id)
    if request.method == "POST":
        comment=Comment.objects.create(commentfield=request.POST["commentfield"],commentid_id=pk,commentprofileid_id=profile.id)
        comment.save()
        return redirect("list")

    else:
        comment=CommentForm()
        return render(request,'commentcreate.html',{"comment":comment})

def sendmessagefunc(request,pk):
    profile=Profile.objects.get(id=pk)
    if request.method == "POST":
        sendmessage = Message.objects.create(message=request.POST["message"],image=request.FILES.get("image"),sendmessageid_id=request.user.id,recievemessageid_id=profile.id)
        # print(recievemessageid_id)
        sendmessage.save()
        return redirect("list")

    else :
        sendmessage=SendMessageForm()
        return render(request,"sendmessage.html",{"sendmessage":sendmessage})

def messagelistfunc(request,pk):
    send_message_list = Message.objects.filter(sendmessageid_id=pk).order_by("created_at").reverse()
    profile=Profile.objects.get(profileid_id=pk)
    recieve_message_list = Message.objects.filter(recievemessageid_id=profile.id).order_by("created_at").reverse()
    profile_list=[]
    profile_list1=[]
    profile_list2=[]
    sender_list=[]
    reciever_list=[]
    new_recieve_message_list=[]
    new_send_message_list=[]
    for i in recieve_message_list.values("sendmessageid_id"):
        profile_list.append(i["sendmessageid_id"])

    for v in send_message_list.values("recievemessageid_id"):
        profile_list1.append(v["recievemessageid_id"])
        profile_list2.append(v["recievemessageid_id"])

    for s in profile_list:
        profile=Profile.objects.get(profileid_id=s)
        sender_list.append(profile.username)

    for w in profile_list2:
        profile2=Profile.objects.get(id=w)
        reciever_list.append(profile2.username)

    for t in range(len(recieve_message_list)):
        sender=model_to_dict(recieve_message_list[t])
        sender["username"]=sender_list[t]
        new_recieve_message_list.append(sender)

    for u in range(len(send_message_list)):
        reciever=model_to_dict(send_message_list[u])
        reciever["recieverid"]=profile_list1[u]
        reciever["username"]=reciever_list[u]
        print(reciever)
        new_send_message_list.append(reciever)

    if len(new_send_message_list) == 0 :
        if len(new_recieve_message_list) == 0 :
            return render(request,"messagelist.html",{"send_list":"送信メッセージはありません","recieve_list":"受信メッセージはありません"})
        else:
            return render(request,"messagelist.html",{"send_list":"送信メッセージはありません","new_recieve_message_list":new_recieve_message_list})
    else:
        if len(new_recieve_message_list) == 0 :
            return render(request,"messagelist.html",{"new_send_message_list":new_send_message_list,"recieve_list":"受信メッセージはありません"})
        else:
            return render(request,"messagelist.html",{"new_send_message_list":new_send_message_list,"new_recieve_message_list":new_recieve_message_list})



















# def profileupdatefunc(request,pk):
#     profile_update=Profile.objects.get(profileid=pk)
#     if request.method == "POST":
#         profile_update.username=request.POST["username"]
#         profile_update.age=request.POST["age"]
#         profile_update.sex=request.POST["sex"]
#         profile_update.icon=request.POST["icon"]
#         profile_update.save()
#         return redirect("list")
#
#
#     else:
#         return render(request,"profileupdate.html",{"profile_update":profile_update})




# def profilefunc(request) :
#
#     if request.method == "POST":
#         profileform = ProfileForm(request.POST,request.FILES)
#         if profileform.is_valid():
#         try :
#         profileform = ProfileForm()
#             print(request.POST["age"])
#             profileform.age = request.POST["age"]
#             profileform.sex = request.POST["sex"]
#             profileform.address = request.POST["address"]
#             profileform.icon = request.FILES["icon"]
#             print(profileform.icon)
#             print(profileform.age)
#             profileform.save()
#         return redirect("list")
#         except Exception as e:
#             print(e)
#             # profileform.save()
#             return redirect("profile")
#
#
#     else :
#         profileform = ProfileForm(request.GET)
#         return render(request,"profile.html",{"profileform":profileform})






# def loginfunc(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#         else:
#             return redirect('login')
#     else :
#         loginform = LoginForm()
#         return render(request,'login.html',{'loginform':loginform})
#     return redirect('list')
#
# def logoutfunc(request):
#     logout(request)
#     return redirect("login")
