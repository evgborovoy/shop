from django.urls import path
from .views import get_cookie_view, set_cookie_view, get_session_view, set_session_view, MyLogoutView, MyLoginView

app_name = "myauth"

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("cookie/get/", get_cookie_view, name="cookie_get"),
    path("cookie/set/", set_cookie_view, name="cookie_set"),
    path("session/set/", set_session_view, name="session_set"),
    path("session/get/", get_session_view, name="session_get"),
]
