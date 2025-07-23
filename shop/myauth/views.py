from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy


class MyLoginView(LoginView):
    template_name = "myauth/login.html"
    redirect_authenticated_user = True


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("foo", "bar", max_age=1800)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("foo", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default session")
    return HttpResponse(f"Session value: {value!r}")
