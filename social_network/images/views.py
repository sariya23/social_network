from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist

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
    return render(request, "images/image/create.html",
                  {"section": "images", "form": form, "title": "Загрузить картинку"})


@login_required
@require_POST
def image_like(request: HttpRequest):
    image_id = request.POST.get("id")
    action = request.POST.get("action")

    if image_id and action:
        image = get_object_or_404(Image, pk=image_id)
        if action == "like":
            image.user_like.add(request.user)
        else:
            image.user_like.remove(request.user)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "ok"})


@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")
    images_for_page = None

    try:
        images_for_page = paginator.page(page)
    except PageNotAnInteger:
        images_for_page = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images_for_page = paginator.page(paginator.num_pages)

    if images_only:
        return render(request, "images/image/list_images.html", {"section": "images", "images": images_for_page, "title": "Картинки"})
    return render(request, "images/image/list.html", {"section": "images", "images": images, "title": "Картинки"})
