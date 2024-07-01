from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(extra_context={"title": "Login"}), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("password-change/", views.CustomPasswordChange.as_view(extra_context={"title": "Сменить пароль"}),
         name="password_change"),
    path("password-change/done/", auth_views.PasswordChangeDoneView.as_view(extra_context={"title": "Login"}),
         name="password_change_done"),
    path("password-reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset-done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(extra_context={"title": "Login"}),
         name="password_reset_complete"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="list"),
    path("users/follow/", views.user_follow, name="follow"),
    path("users/<username>/", views.user_detail, name="detail")
]
