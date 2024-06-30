from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ImageForm
from .models import Image


def image_detail(request: HttpRequest, image_id: int, slug: str) -> HttpResponse:
    image = get_object_or_404(Image, pk=image_id, slug=slug)
    return render(request, "images/image/detail.html", {"section": "images", "image": image, "title": image.title})


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
