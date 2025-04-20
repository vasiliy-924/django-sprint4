from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils import timezone

from .models import Comment, Post

User = get_user_model()


class UserEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pub_date"].initial = timezone.localtime(
            timezone.now()
        ).strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = Post
        fields = ["title", "text", "image", "pub_date", "category", "location"]
        widgets = {
            "pub_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
