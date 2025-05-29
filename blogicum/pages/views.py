from django.views.generic import TemplateView


class AboutView(TemplateView):
    """
    Отображает страницу "О проекте".
    
    Attributes:
        template_name: Путь к шаблону страницы
    """
    template_name = "pages/about.html"


class RulesView(TemplateView):
    """
    Отображает страницу с правилами использования сайта.
    
    Attributes:
        template_name: Путь к шаблону страницы
    """
    template_name = "pages/rules.html"


class CsrfFailureView(TemplateView):
    """
    Отображает страницу с ошибкой CSRF-защиты.
    
    Attributes:
        template_name: Путь к шаблону страницы
    """
    template_name = "pages/403csrf.html"


class PageNotFoundView(TemplateView):
    """
    Отображает страницу с ошибкой 404 (страница не найдена).
    
    Attributes:
        template_name: Путь к шаблону страницы
    """
    template_name = "pages/404.html"


class ServerErrorView(TemplateView):
    """
    Отображает страницу с ошибкой 500 (внутренняя ошибка сервера).
    
    Attributes:
        template_name: Путь к шаблону страницы
    """
    template_name = "pages/500.html"
