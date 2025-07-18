from django import forms
from .models import Image
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        # ? provoding images from an external site on frontend
        widgets = {
            'url': forms.HiddenInput(),
        }

    # ? validate url
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given URL doesn't match valid image extensions")

        return url

    # ! keeping the parameters required by ModelForm
    def save(self, force_insert=False, force_update=False, commit=True):
        # a new image instance is created by calling the save() method
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        response = requests.get(image_url)
        # ? ContentFile(response.content) wraps the image bytes and store it to image field
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()

        return image