from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.http import Http404
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
# Create your views here.

""" ? Advantages of class-based views
    - Organize code related to HTTP methods, such as GET, POST, or PUT, in separate methods, instead of using conditional branching
    - Use multiple inheritance to create reusable view classes (also known as mixins)
"""
# class PostListView(ListView):
#     queryset = Post.published.all() # custom QuerySet, default would be QuerySet Post.objects.all()
#     context_object_name = 'posts' # the default variable is object_list for the query results
#     paginate_by = 3
#     template_name = 'blog/post/list.html' # if not specified, post_list.html is used

    #? class-based view provides HTTP 404 status for exception handling, in this case, of pagination

def post_list(request, tag_slug=None):
    #! request is the HttpRequest instance passed from url pattern matching
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    #? Pagination with 3 posts per page
    paginator = Paginator(post_list, 3) #? instantiate the Paginator object with the number of objects to return per page
    page_number = request.GET.get('page', 1) #?page=page_number

    try:
        posts = paginator.page(page_number) # Paginator instance retrieves only three pages
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    #! render function renders HttpResponse object with the rendered text
    # <HttpResponse status_code=200, "text/html; charset=utf-8">
    return render(request, 'blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    # try:
    #     post = Post.published.get(pk=pk)
    # except Post.DoesNotExist:
    #     raise Http404("Post does not exist")

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day
                             )

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # list of similar posts
    # ? the query returns values for the given field: id in this case
    # ? flat=True return [1,2,3,...] instead of [(1,), (2,), (3,) ...]
    post_tags_ids = post.tags.values_list('id', flat=True)
    # ? get all posts corresponding to the ids list
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # ? aggregate count for the posts sharing the same tag
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   "comments": comments,
                   'form': form,
                   'similar_posts': similar_posts
                   })

def post_share(request, post_id):

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        #! if the form is invalid, the form is rendered in the template again, including the data submitted
        if form.is_valid():
            #? retrieving cleaned values of form in dictionary format {fields: values}
            cleaned_data = form.cleaned_data

            #? building a complete url including HTTP schema and hostname
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = (f"{cleaned_data['name']} ({cleaned_data['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cleaned_data['name']}\'s comments: {cleaned_data['comments']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None, #? DEFAULT_FROM_EMAIL is used for setting None
                recipient_list=[cleaned_data['to']]
            )
            sent = True

    else:
        form = EmailPostForm()

    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

@require_POST
def post_comment(request, post_id):

    form = CommentForm(data=request.POST)
    # Create a Comment object without saving it to the database
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    if form.is_valid():

        #? commit=False is allowed for ModelForm
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    return render(
            request,
            'blog/post/comment.html',
            {
                'post': post,
                'form': form,
                'comment': comment
            }
        )

def post_search(request):
    # ? use GET request to fetch query from request
    form = SearchForm(request.GET)
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            # #? search query by default provides stemming algorithms
            # search_query = SearchQuery(query)
            # #? ordering results by relevancy
            # results = (
            #     Post.published.annotate(
            #         search=search_vector,
            #         rank=SearchRank(search_vector, search_query)
            #     ).filter(rank__gte=0.3)
            #     .order_by('-rank')
            # )

            results = (
                Post.published.annotate(
                    similarity = TrigramSimilarity('title', query)
                ).filter(similarity__gte=0.1)
                .order_by('-rank')
            )

    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )