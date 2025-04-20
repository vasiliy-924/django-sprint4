from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "pages/about.html"


class RulesView(TemplateView):
    template_name = "pages/rules.html"


class CsrfFailureView(TemplateView):
    template_name = "pages/403csrf.html"


class PageNotFoundView(TemplateView):
    template_name = "pages/404.html"


class ServerErrorView(TemplateView):
    template_name = "pages/500.html"
