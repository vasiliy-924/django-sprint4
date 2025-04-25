from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def csrf_failure(request, reason=""):
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)


def server_error(request):
    return render(request, "pages/500.html", status=500)


def registration(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")

    return render(
        request,
        "registration/registration_form.html",
        {"form": form}
    )
