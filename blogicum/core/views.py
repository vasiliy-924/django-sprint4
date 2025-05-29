from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def csrf_failure(request, reason=""):
    """
    Обрабатывает ошибку CSRF-защиты.
    
    Args:
        request: HTTP запрос
        reason: Причина ошибки CSRF
        
    Returns:
        HttpResponse: Страница с ошибкой 403
    """
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    """
    Обрабатывает ошибку 404 (страница не найдена).
    
    Args:
        request: HTTP запрос
        exception: Исключение, вызвавшее ошибку
        
    Returns:
        HttpResponse: Страница с ошибкой 404
    """
    return render(request, "pages/404.html", status=404)


def server_error(request):
    """
    Обрабатывает ошибку 500 (внутренняя ошибка сервера).
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Страница с ошибкой 500
    """
    return render(request, "pages/500.html", status=500)


def registration(request):
    """
    Обрабатывает регистрацию новых пользователей.
    
    Args:
        request: HTTP запрос
        
    Returns:
        HttpResponse: Страница регистрации или редирект на страницу входа
    """
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")

    return render(
        request,
        "registration/registration_form.html",
        {"form": form}
    )
