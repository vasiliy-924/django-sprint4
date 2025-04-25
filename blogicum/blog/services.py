from django.core.paginator import Paginator
from .constants import POSTS_LIMIT


def get_paginated_page(request, queryset, per_page=POSTS_LIMIT):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))
