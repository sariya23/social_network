from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'account'

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(extra_context={"title": "Login"}), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.dashboard, name="dashboard"),
]