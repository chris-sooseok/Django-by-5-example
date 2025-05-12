from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
# Create your views here.


def post_list(request):
    #! request is the HttpRequest instance passed from url pattern matching
    posts = Post.published.all()

    #! render function renders HttpResponse object with the rendered text
    # <HttpResponse status_code=200, "text/html; charset=utf-8">
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, pk):
    # try:
    #     post = Post.published.get(pk=pk)
    # except Post.DoesNotExist:
    #     raise Http404("Post does not exist")
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)

    return render(request, 'blog/post/detail.html', {'post': post})

