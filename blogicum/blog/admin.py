from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post

admin.site.site_header = "Панель администратора Блога"
admin.site.site_title = "Администрирование блога"
admin.site.index_title = "Добро пожаловать в админ-панель Блога"
admin.site.empty_value_display = "Не задано"

admin.site.unregister(Group)

User = get_user_model()
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "posts_count",
        "comments_count",
    )
    list_display_links = ("username", "email")

    @admin.display(description="Кол-во постов")
    def posts_count(self, obj):
        return obj.posts.count() if hasattr(obj, "posts") else 0

    @admin.display(description="Кол-во комментариев")
    def comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, "comments") else 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "is_published")
    list_editable = ("is_published",)
    search_fields = ("title",)
    list_display_links = ("title",)

    @admin.display(description="Описание")
    def short_description(self, obj):
        return obj.description[:100] + "..." if obj.description else ""


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_display_links = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pub_date",
        "author",
        "location",
        "category",
        "is_published",
        "safe_short_text",
        "display_image",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "text")
    list_filter = ("category", "location", "author")
    date_hierarchy = "pub_date"
    list_display_links = ("title",)
    list_select_related = ("author", "location", "category")

    @admin.display(description="Краткий текст")
    def safe_short_text(self, obj):
        if not obj.text:
            return ""
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text

    @admin.display(description="Изображение")
    def display_image(self, obj):
        if obj.image and obj.image.storage.exists(obj.image.name):
            return mark_safe(
                f'<img src="{obj.image.url}" width="80" height="60">'
            )
        return "Нет изображения"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "short_text",
        "author",
        "post",
        "created_at",
        "is_published",
    )
    list_editable = ("is_published",)
    search_fields = ("text",)
    list_filter = ("is_published", "post")
    list_select_related = ("author", "post")
    date_hierarchy = "created_at"

    @admin.display(description="Текст")
    def short_text(self, obj):
        return f"{obj.text[:100]}..." if len(obj.text) > 100 else obj.text
