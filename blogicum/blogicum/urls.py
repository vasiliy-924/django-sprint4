from core.views import registration
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

handler403 = "core.views.csrf_failure"
handler404 = "core.views.page_not_found"
handler500 = "core.views.server_error"

# В Шаблоне обычная ссылка, она делает GET /auth/logout/, а это вызывает 405.
# Т.к. шаблоны html менять запрещено по ТЗ -> создаем кастомный logout.


class LogoutGetAllowed(LogoutView):
    template_name = "registration/logged_out.html"
    http_method_names = ["get", "post", "head", "options", "trace"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    # Авторизация
    path("auth/logout/", LogoutGetAllowed.as_view(), name="logout"),
    path("auth/registration/", registration, name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path("pages/", include("pages.urls")),
    path(
        "accounts/profile/",
        RedirectView.as_view(url="/profile/"),
        name="profile_redirect",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
