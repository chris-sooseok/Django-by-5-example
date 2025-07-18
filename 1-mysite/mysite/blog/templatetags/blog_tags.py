from django import template
from ..models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

"""
? {% load blog_tags %} will load template tags and filters you defined here
? After loading, use the function name to provide features
"""

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()

#! the template specified in the tag will be rendered with the return values
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]

    #? inclusion tag must return a dictionary
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
    total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    # ? Django by default escape all HTML element
    # ? mark_safe prevents escaping and set markdown formatting
    return mark_safe(markdown.markdown(text))