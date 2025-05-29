from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils import timezone

from .models import Comment, Post

User = get_user_model()


class UserEditForm(UserChangeForm):
    """
    Форма для редактирования профиля пользователя.
    Позволяет изменять имя, фамилию, имя пользователя и email.
    """
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")


class PostForm(forms.ModelForm):
    """
    Форма для создания и редактирования поста.
    Включает все поля модели Post, кроме is_published и author.
    Поддерживает загрузку изображений и установку даты публикации.
    """
    pub_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local"},
        ),
        input_formats=[
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
        ],
    )

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и устанавливает текущее время
        как значение по умолчанию для поля pub_date.
        """
        super().__init__(*args, **kwargs)
        self.fields["pub_date"].initial = timezone.localtime(
            timezone.now()
        ).strftime("%Y-%m-%dT%H:%M")

    class Meta:
        model = Post
        exclude = ("is_published", "author")
        widgets = {
            "pub_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}
            )
        }


class CommentForm(forms.ModelForm):
    """
    Форма для создания и редактирования комментария.
    Содержит только поле text для ввода текста комментария.
    """
    class Meta:
        model = Comment
        fields = ("text",)
