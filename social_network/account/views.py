from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login

from .forms import LoginForm


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Success")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})