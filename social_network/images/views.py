from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ImageForm


@login_required
def image_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ImageForm(request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Картинка добавлена успешно")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageForm(request.GET)
    return render(request, "images/image/create.html", {"section": "images", "form": form, "title": "Загрузить картинку"})
