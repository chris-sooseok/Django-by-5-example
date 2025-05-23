from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
from django.urls import reverse
from taggit.managers import TaggableManager

""" 
? Python class is a collection of data and methods.
? Classes are the blueprint for bundling data and functionality together.
? Creating a new class creates a new type of object, allowing you to create instances of that type

? A Django model is a source of information about the behaviors of your data. It consists of a Python
? class that subclasses django.db.models.Model. Each model maps to a single database table, where
? each attribute of the class represents a database field.

? When you create a model, Django will provide you with a practical API to query objects in the database easily.
? We will define the database models for our blog application. Then, we will generate the database migrations
? for the models to create the corresponding database tables. When applying the migrations,
? Django will create a table for each model defined in the models.py file of the application. """


class PublishedManager(models.Manager):
    """
    ? creating a custom query set to facilitate published post retrieve
    """
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(models.Model):

    objects = models.Manager() # ? original QuerySet provided by Django
    published = PublishedManager()

    #! if primary key is not specified, DEFAULT_AUTO_FIELD from apps.py is applied.

    title = models.CharField(max_length=250) # translates to VARCHAR in db

    #? creating an unique slug for the date stored in publish field. This enforcement is not done in database level
    #! preventing a new post with the same slug from the same date
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish') # translates to VARCHAR in db, used to build a beautiful URL

    """? 
    ? Django comes with an auth framework that handles user accounts. The Django authentication framework comes in the django.contrib.auth
    ? package and contains a User model. To define the relationship between users and posts, we will use the AUTH_USER_MODEL setting, which points to 
    ? auth.User by default. This setting allows you to specify a different user model for your project. """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")

    body = models.TextField() # translates to TEXT in db
    publish = models.DateTimeField(default=timezone.now) # translates to DATETIME

    # publish = models.DateTimeField(db_default=Now()) uses database-computed default value
    created = models.DateTimeField(auto_now_add=True) # save date and time when created
    updated = models.DateTimeField(auto_now=True) # update date and time when updated

    # ?  enumeration class by subclassing models.TextChoices
    # ?  https://docs.python.org/3/library/enum.html
    # ?  https://docs.djangoproject.com/en/5.0/ref/models/fields/#enumeration-types
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    #? We can access Post.Status.choices to obtain the available choices, Post.Status.names to obtain the
    #? names of the choices, Post.Status.labels to obtain the human-readable names, and Post.Status.
    #? values to obtain the actual values of the choices.
    status = models.CharField(
        max_length=2,
        choices=Status, # limit the value of the field to be Status parameters
        default=Status.DRAFT,
    )

    tags = TaggableManager() # adding Tag application

    class Meta:
        #! reverse ordering to show the newest posts first.
        #! This ordering takes effect when retrieving objects from the database
        ordering = ['-publish']
        #! This will improve performance for query filtering or ordering results by this field. We expect many queries to take advantage of this index since we are
        #! using the publish field to order results by default.
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    #? reverse function will build the URL address dynamically using the URL name defined in the URL patterns
    #? <a href="{% url 'blog:post_detail' post.id %}"> to <a href="{{ post.get_absolute_url }}">
    #? /post_id to /year/month/day/slug
    def get_absolute_url(self):
        return reverse("blog:post_detail",
                       args=[
                           self.publish.year,
                           self.publish.month,
                           self.publish.day,
                           self.slug
                       ])


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
