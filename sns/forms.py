from django import forms
from .models import Profile,Keijiban,Comment,Message


class KeijibanForm(forms.ModelForm) :
    class Meta :
        model = Keijiban
        fields = "__all__"

class CreateForm(forms.ModelForm):
    class Meta :
        model = Keijiban
        fields = ["toukou","image"]

class ProfileForm(forms.ModelForm):
    class Meta :
        model = Profile
        fields = ["username","age","sex","address","icon"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["commentfield"]

class SendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["message","image"]
