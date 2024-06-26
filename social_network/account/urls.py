from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = 'account'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(extra_context={"title": "Login"}), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("password-change/", views.CustomPasswordChange.as_view(), name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view() ,name="password_change_done"),
    path("", views.dashboard, name="dashboard"),
]