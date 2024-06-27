from django import forms
from django.core.files.base import ContentFile
import requests

from .models import Image
from .models import translate_to_english


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,

        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = {"jpg", "jpeg", "png"}
        extension = url.split(".")[-1].lower()

        if extension not in valid_extensions:
            raise forms.ValidationError("Неподдерживаемый формат изображения")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = translate_to_english(image.title)
        extension = image_url.split(".", 1)[-1].lower()
        image_name = f"{name}.{extension}"
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()
        return image