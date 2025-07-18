from django.contrib import admin
from .models import Post, Comment
# Register your models here.

# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/.

# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ['title', 'body'] # add search bar
    prepopulated_fields = {'slug': ('title',)} # allows automatic fill-in
    raw_id_fields = ['author'] # generate a lookup widget for authors
    date_hierarchy = 'publish' # add date hierarchy navigation bar
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS # add counts for each filter

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']