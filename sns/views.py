from django.shortcuts import render,redirect
from .forms import KeijibanForm,ProfileForm,CreateForm,CommentForm,SendMessageForm
from django.contrib.auth import authenticate, login, logout
from .models import Keijiban,Profile,Comment,Message
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
#追加
from django.template.loader import render_to_string
from django.http import JsonResponse




def listfunc(request,now_page=1):
    object_list=Keijiban.objects.all().order_by("created_at").reverse()
    comment_list=Comment.objects.all().order_by("created_at").reverse()

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
    try:
        Profile.objects.get(profileid_id=request.user.id)
        if request.method == "POST":
            form = Keijiban.objects.create(toukou=request.POST["toukou"],image=request.FILES.get("image"),authorid_id=request.user.id)
            return redirect("list")

        else:
            createform = CreateForm()
            return render(request,"create.html",{"createform":createform})
    except:
        return redirect("profile")

def profilefunc(request):
    if request.method == "POST":
        if int(request.POST["age"]) > 150 :
            obj=Profile()
            print(obj)
            profileform = ProfileForm(request.POST,request.FILES,instance=obj)
            return render(request,"profile.html",{"profileform":profileform})

        else:
            profileform = Profile.objects.create(username=request.POST["username"],age=request.POST["age"],sex=request.POST["sex"],address=request.POST["address"],icon=request.FILES.get("icon"),profileid_id=request.user.id)
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

@login_required
def profileupdatefunc(request):
    try:
        Profile.objects.get(profileid_id=request.user.id)
        obj=Profile.objects.get(profileid_id=request.user.id)
        if request.method == "POST":
            profile_update=ProfileForm(request.POST,request.FILES,instance=obj)
            if profile_update.is_valid():
                profile_update.save()
                return redirect("list")
            else:
                return render(request,"profileupdate.html",{"profile_update":profile_update})

        else:
            profile_update=ProfileForm(instance=obj)
            return render(request,"profileupdate.html",{"profile_update":profile_update,"obj":obj})
    except:
        return redirect("profile")

@login_required
def keijibanupdatefunc(request,pk):
    try:
        Profile.objects.get(profileid_id=request.user.id)
        obj=Keijiban.objects.get(id=pk)
        if request.method == "POST":
            keijiban_update=CreateForm(request.POST,request.FILES,instance=obj)
            keijiban_update.save()
            return redirect("list")

        else:
            keijiban_update=CreateForm(instance=obj)
            return render(request,"keijibanupdate.html",{"keijiban_update":keijiban_update,"obj":obj})
    except:
        return redirect("profile")

@login_required
def keijibandeletefunc(request,pk):
    try:
        Profile.objects.get(profileid_id=request.user.id)
        obj=Keijiban.objects.get(id=pk)
        if request.method == "POST":
            obj.delete()
            return redirect("list")

        else:
            keijiban_delete=KeijibanForm(instance=obj)
            return render(request,"keijibandelete.html",{"keijiban_delete":keijiban_delete,"obj":obj})
    except:
        return redirect("profile")

@login_required
def goodfunc(request,pk):
    try:
        Profile.objects.get(profileid_id=request.user.id)

        keijiban=Keijiban.objects.get(id=pk)
        goodman = Profile.objects.get(profileid_id=request.user.id).username
        if goodman in keijiban.goodtext :
            return redirect("list")

        else:
            keijiban.goodtext = keijiban.goodtext + " " + goodman + "さん"
            keijiban.good+=1
            keijiban.save()
            return redirect("list")
    except:
        return redirect("profile")



@login_required
def commentcreatefunc(request,pk):
    try:
        profile=Profile.objects.get(profileid_id=request.user.id)
        if request.method == "POST":
            comment=Comment.objects.create(commentfield=request.POST["commentfield"],commentid_id=pk,commentprofileid_id=profile.id)
            comment.save()
            return redirect("list")

        else:
            comment=CommentForm()
            return render(request,'commentcreate.html',{"comment":comment})
    except:
        return redirect("profile")

@login_required
def sendmessagefunc(request,pk):
    try:
        profile=Profile.objects.get(profileid_id=request.user.id)

        profile=Profile.objects.get(profileid_id=pk)
        if request.method == "POST":
            sendmessage = Message.objects.create(message=request.POST["message"],image=request.FILES.get("image"),sendmessageid_id=request.user.id,recievemessageid_id=profile.id)
            sendmessage.save()
            return redirect("list")

        else :
            sendmessage=SendMessageForm()
            return render(request,"sendmessage.html",{"sendmessage":sendmessage})
    except:
        return redirect("profile")

@login_required
def messagelistfunc(request,pk):
    try:
        profile=Profile.objects.get(profileid_id=request.user.id)

        send_message_list = Message.objects.filter(sendmessageid_id=pk).order_by("created_at").reverse()  #ログインしている人が送ったメッセージ一覧
        profile=Profile.objects.get(profileid_id=pk)
        recieve_message_list = Message.objects.filter(recievemessageid_id=profile.id).order_by("created_at").reverse() #ログインしている人が受け取ったメッセージ一覧

        profile_list=[]
        profile_list1=[]
        profile_list2=[]
        sender_list=[]
        sender_icon_list=[]
        reciever_list=[]
        reciever_icon_list=[]
        new_recieve_message_list=[]
        new_send_message_list=[]
        for i in recieve_message_list.values("sendmessageid_id"):  #ログインしている人が受け取ったメッセージ一覧から送信者を出す
            profile_list.append(i["sendmessageid_id"])             #送信者のsendmessageid_idをリストにする

        for v in send_message_list.values("recievemessageid_id"): #ログインしている人が送ったメッセージ一覧から受信する人を抽出
            profile_list2.append(v["recievemessageid_id"])        #受信する人のidをリストにする

        for s in profile_list:
            profile=Profile.objects.get(profileid_id=s)           #送信者のprofile情報を取得
            sender_list.append(profile.username)                  #送信者の名前をリストにする
            sender_icon_list.append(profile.icon)                 #送信者のiconをリストにする

        for w in profile_list2:
            profile2=Profile.objects.get(id=w)                    #受信者のprofile情報を取得
            reciever_list.append(profile2.username)               #受信者の名前をリストにする
            reciever_icon_list.append(profile2.icon)              #受信者のiconをリストにする

        for t in range(len(recieve_message_list)):
            sender=model_to_dict(recieve_message_list[t])         #ログインしている人が受信するメッセージリスト(QuerySet)を辞書にする
            sender["username"]=sender_list[t]                     #送信者名を辞書に追加
            sender["icon"]=sender_icon_list[t]                    #送信者iconを辞書に追加
            new_recieve_message_list.append(sender)               #ログインしている人が受信するメッセージ一覧に送信者を追加

        for u in range(len(send_message_list)):
            reciever=model_to_dict(send_message_list[u])          #ログインしている人が送信したメッセージリスト(QuerySet)を辞書にする
            profileid=Profile.objects.get(id=profile_list2[u])    #受信する人のidがprofileのidと一致するprofile情報を取得
            reciever["recieverid"]=profileid.profileid_id         #取得したprofile情報からprofileid_id(ユーザーモデルのid)を取得して受信者として辞書に追加
            reciever["username"]=reciever_list[u]                 #受信者の名前を辞書に追加
            reciever["icon"]=reciever_icon_list[u]                #受信者のiconを辞書に追加
            new_send_message_list.append(reciever)                #ログインしている人が送ったメッセージ一覧に受信者を追加


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

    except:
        return redirect("profile")


def guest_login(request):
    guest_user = CustomUser.objects.get(email="guestuser@example.com")
    login(request, guest_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('list')
