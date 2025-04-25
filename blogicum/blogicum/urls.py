from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import registration

handler403 = "core.views.csrf_failure"
handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    # Авторизация
    path("auth/registration/", registration, name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path("pages/", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
