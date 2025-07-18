from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Image
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from actions.utils import create_action
import redis
from django.conf import settings

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
            messages.success(request, 'Image created')
            return redirect(new_image.get_absolute_url())

    else:
        # build form with data provided by the bookmarklet via GET
        # this data will consist of url and title attributes from an externl website
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {"section": "images", "form": form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # ? increment or create if not exist
    total_views = r.incr(f'image:{image.id}:views')
    # ? sore views in a sorted set with image:ranking key
    r.zincrby('image_ranking', 1, image.id)
    return render(
        request,
    'images/image/detail.html',
    {
        'section': 'images',
        'image': image,
        'total_views': total_views
            }
)

@login_required
def image_ranking(request):
    # zrange to obtain the elements in the sorted set
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]

    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(
        request,
        'images/image/ranking.html',
        {'section': 'images', 'most_viewed': most_viewed}
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
                create_action(request.user, 'likes', image)
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
        return render(request,
                      'images/image/list_images.html',
                      {'section': 'images', 'images': images}
                      )
    return render(
        request,
        'images/image/list.html',
        {'section': 'images', 'images': images}
    )
