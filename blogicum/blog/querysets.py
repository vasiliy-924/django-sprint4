from django.utils import timezone


def filter_posts_by_publication(queryset):
    return queryset.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    ).select_related("category", "location", "author")
