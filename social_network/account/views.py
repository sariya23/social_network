from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "account/dashboard.html", {"section": "dashboard", "title": "Dashboard"})


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse("account:dashboard"))


class CustomPasswordChange(PasswordChangeView):
    success_url = reverse_lazy("account:password_change_done")