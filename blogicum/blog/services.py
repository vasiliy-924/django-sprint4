from django.core.paginator import Paginator

from .constants import POSTS_LIMIT


def get_paginated_page(request, queryset, per_page=POSTS_LIMIT):
    """
    Создает пагинированную страницу для переданного QuerySet.
    
    Args:
        request: HTTP запрос, содержащий параметр page
        queryset: QuerySet для пагинации
        per_page: Количество объектов на странице (по умолчанию POSTS_LIMIT)
        
    Returns:
        Page: Объект страницы с пагинированными данными
    """
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))
