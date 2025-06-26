from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()

            messages.success(request, 'Image created')
            return redirect(new_image.get_absolute_url())

    else:
        # build form with data provided by the bookmarklet via GET
        # this data will consist of url and title attributes from an externl website
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {"section": "images", "form": form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request,
    'images/image/detail.html',
    {'section': 'images', 'image': image}
)

@login_required
@require_POST
def image_like(request):
    """
    expects two POST parameters: image_id and action
    """
    print(1)
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # add or remove object to relationship
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    # if the whole HTML or only new images
    images_only = request.GET.get('images_only')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # If AJAX request and page out of range, return an empty page
            # this allows you to stop AJAX pagination on the client side when reaching the last page
            return HttpResponse('')

    if images_only:
        print(2)
        return render(request,
                      'images/image/list_images.html',
                      {'section': 'images', 'images': images}
                      )

    print(1)
    return render(
        request,
        'images/image/list.html',
        {'section': 'images', 'images': images}
    )
