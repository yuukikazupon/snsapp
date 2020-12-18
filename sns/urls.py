from django.urls import path
from .views import listfunc,createfunc,profilefunc,profiledetailfunc,profileupdatefunc,keijibandeletefunc,\
    keijibanupdatefunc,goodfunc,commentcreatefunc
from django.conf.urls import url


urlpatterns = [
    path("list/<int:now_page>/",listfunc,name="list"),
    path("list/",listfunc,name="list"),
    path("create/",createfunc,name="create"),
    path("",profilefunc,name="profile"),
    path("profiledetail/<int:pk>/",profiledetailfunc,name="profiledetail"),
    path("profileupdate/",profileupdatefunc,name="profileupdate"),
    path("keijibandelete/<int:pk>/",keijibandeletefunc,name="keijibandelete"),
    path("keijibanupdate/<int:pk>/",keijibanupdatefunc,name="keijibanupdate"),
    path("good/<int:pk>",goodfunc,name="good"),
    path("commentcreate/<int:pk>",commentcreatefunc,name="commentcreate"),



]
