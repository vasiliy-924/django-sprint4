from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .constants import (
    CHARFIELD_MAX_LENGTH,
    DEFAULT_STR_LENGTH,
    PUBLISHED_HELP_TEXT,
    SLUGFIELD_MAX_LENGTH,
)

User = get_user_model()


class PostQuerySet(models.QuerySet):
    """
    Кастомный QuerySet для модели Post с дополнительными методами фильтрации.
    """
    
    def filter_posts_by_publication(self):
        """
        Фильтрует посты по следующим критериям:
        - пост опубликован
        - категория поста опубликована
        - дата публикации не в будущем
        
        Returns:
            QuerySet: Отфильтрованный набор постов
        """
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )

    def annotate_comment_count(self):
        """
        Добавляет к постам аннотацию с количеством комментариев
        и сортирует по дате публикации (новые сверху).
        
        Returns:
            QuerySet: Набор постов с количеством комментариев
        """
        return self.annotate(
            comment_count=models.Count("comments")
        ).order_by("-pub_date")


class CreatedAtAbstract(models.Model):
    """
    Абстрактная модель с полем даты создания.
    Используется как базовая модель для других моделей.
    """
    created_at = models.DateTimeField(
        "Добавлено", auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ("created_at",)
        default_related_name = "%(app_label)s_%(class)s"


class IsPublishedCreatedAtAbstract(CreatedAtAbstract):
    """
    Абстрактная модель с полями даты создания и статуса публикации.
    Наследуется от CreatedAtAbstract.
    """
    is_published = models.BooleanField(
        "Опубликовано", default=True, help_text=PUBLISHED_HELP_TEXT
    )

    class Meta(CreatedAtAbstract.Meta):
        abstract = True


class Post(IsPublishedCreatedAtAbstract):
    """
    Модель поста блога.
    Содержит основную информацию о публикации: заголовок, текст,
    дату публикации, автора, местоположение, категорию и изображение.
    """
    title = models.CharField("Заголовок", max_length=CHARFIELD_MAX_LENGTH)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField(
        "Изображение", upload_to="posts_images/", blank=True, null=True
    )
    objects = PostQuerySet.as_manager()

    class Meta(IsPublishedCreatedAtAbstract.Meta):
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        """
        Возвращает строковое представление поста.
        
        Returns:
            str: Заголовок поста, обрезанный до DEFAULT_STR_LENGTH символов
        """
        return self.title[:DEFAULT_STR_LENGTH]


class Category(IsPublishedCreatedAtAbstract):
    """
    Модель категории постов.
    Содержит название, описание и уникальный slug для URL.
    """
    title = models.CharField("Заголовок", max_length=CHARFIELD_MAX_LENGTH)
    description = models.TextField("Описание")
    slug = models.SlugField(
        verbose_name="Идентификатор",
        max_length=SLUGFIELD_MAX_LENGTH,
        unique=True,
        help_text="Идентификатор страницы для URL; "
        "разрешены символы латиницы, цифры, дефис и подчёркивание.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """
        Возвращает строковое представление категории.
        
        Returns:
            str: Название категории, обрезанное до DEFAULT_STR_LENGTH символов
        """
        return self.title[:DEFAULT_STR_LENGTH]


class Location(IsPublishedCreatedAtAbstract):
    """
    Модель местоположения для постов.
    Содержит название места.
    """
    name = models.CharField("Название места", max_length=CHARFIELD_MAX_LENGTH)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        """
        Возвращает строковое представление местоположения.
        
        Returns:
            str: Название места, обрезанное до DEFAULT_STR_LENGTH символов
        """
        return self.name[:DEFAULT_STR_LENGTH]


class Comment(CreatedAtAbstract):
    """
    Модель комментария к посту.
    Содержит связь с постом, автором и текст комментария.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Публикация",
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
    )
    text = models.TextField(verbose_name="Текст комментария")

    class Meta(CreatedAtAbstract.Meta):
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        """
        Возвращает строковое представление комментария.
        
        Returns:
            str: Текст комментария, обрезанный до DEFAULT_STR_LENGTH символов
        """
        return self.text[:DEFAULT_STR_LENGTH]
