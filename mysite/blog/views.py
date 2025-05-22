from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import EmailPostForm, CommentForm
from .models import Post
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.http import Http404
from django.core.mail import send_mail
# Create your views here.

""" ? Advantages of class-based views
    - Organize code related to HTTP methods, such as GET, POST, or PUT, in separate methods, instead of using conditional branching
    - Use multiple inheritance to create reusable view classes (also known as mixins)
"""
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all() # custom QuerySet, default would be QuerySet Post.objects.all()
    context_object_name = 'posts' # the default variable is object_list for the query results
    paginate_by = 3
    template_name = 'blog/post/list.html' # if not specified, post_list.html is used

    #? class-based view provides HTTP 404 status for exception handling, in this case, of pagination

# def post_list(request):
#     #! request is the HttpRequest instance passed from url pattern matching
#     posts = Post.published.all()
#
#     #? Pagination with 3 posts per page
#     paginator = Paginator(posts, 3) #? instantiate the Paginator object with the number of objects to return per page
#     page_number = request.GET.get('page', 1) #?page=page_number
#
#     try:
#         posts = paginator.page(page_number) # Paginator instance retrieves only three pages
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     #! render function renders HttpResponse object with the rendered text
#     # <HttpResponse status_code=200, "text/html; charset=utf-8">
#     return render(request, 'blog/post/list.html', {'posts': posts})

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

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   "comments": comments,
                   'form': form
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