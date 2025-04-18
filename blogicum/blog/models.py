from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    DEFAULT_STR_LENGTH,
    PUBLISHED_HELP_TEXT,
    CHARFIELD_MAX_LENGTH,
    SLUGFIELD_MAX_LENGTH
)

User = get_user_model()


class IsPublishedCreatedAtAbstract(models.Model):
    is_published = models.BooleanField(  # Поле сохранено с is_
        'Опубликовано',
        default=True,
        help_text=PUBLISHED_HELP_TEXT
    )
    created_at = models.DateTimeField(  # Поле сохранено с at_
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Post(IsPublishedCreatedAtAbstract):
    title = models.CharField('Заголовок', max_length=CHARFIELD_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:DEFAULT_STR_LENGTH]


class Category(IsPublishedCreatedAtAbstract):
    title = models.CharField('Заголовок', max_length=CHARFIELD_MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        max_length=SLUGFIELD_MAX_LENGTH,
        unique=True,
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:DEFAULT_STR_LENGTH]


class Location(IsPublishedCreatedAtAbstract):
    name = models.CharField('Название места', max_length=CHARFIELD_MAX_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:DEFAULT_STR_LENGTH]
