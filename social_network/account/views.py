from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import RegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html", {"section": "dashboard", "title": "Dashboard"})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse("account:dashboard"))


class CustomPasswordChange(PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")
    extra_context = {"title": "Сбросить пароль"}


class CustomPasswordResetDoneView(PasswordResetDoneView):
    success_url = reverse_lazy("account:password_reset_confirm")
    extra_context = {"title": "Сбросить пароль"}


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")
    extra_context = {"title": "Сбросить пароль"}


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            print(user_form.cleaned_data["password1"])
            new_user.set_password(user_form.cleaned_data["password1"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user, "title": "Регистрация"})
    else:
        user_form = RegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form, "title": "Регистрация"})


@login_required
def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль обновлен")
        else:
            messages.error(request, "Ошибка в обновлении профиля")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, "account/edit.html", {"user_form": user_form, "profile_form": profile_form, "title": "Редактирование"})


@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    users = User.objects.filter(is_active=True)
    return render(request, "account/user/list.html", {"section": "people", "users": users, "title": "Пользователи"})

@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "account/user/detail.html", {"section": "people", "user": user, "title": username})