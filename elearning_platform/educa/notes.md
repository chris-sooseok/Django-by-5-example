
# Chapter 12: building e-learning platform

# building course models
Each course will be divided into a configurable number of modules, and each module will contain a configurable number of contents.

# Using fixtures to provide initial data for models

dumpdata: dumps data from db into the standard output. The resulting data structure includes information about the model and its fields for django to be able to load it into db
loaddata: load data structure into db

# Creating models for polymorphic content
django offers three options to use model inheritance
- abstract models: Useful when you want to put some common information into several models
- Multi-table model inheritance: In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship between the child model and its parent model
- Proxy models: Useful when you need to change the behavior of a model, for example, by including additional methods, changing the default manager, or using different meta options

# Creating custom model fields
you can also create your own model fields to store custom data or alter the behavior of existing
fields. Custom fields allow you to store unique data types, implement custom validations, encapsulate
complex data logic related to the field, or define specific rendering forms using custom widgets.

# Chapter 13: Creating a content management system

# class-based views
When you need to provide a specific behavior for several class-based views, it is recommended that you use mixins.
Mixins are a type of class designed to supply methods to other classes but aren’t intended to be used independently. This allows you to develop shared functionalities that can be incorporated into various classes in a modular manner, simply by having those classes inherit from mixins. 
The concept is similar to a base class, but you can use multiple mixins to extend the funtionality of a given class

# Working with groups and permissions
By default, Django generates four permissions for each model in the installed applications: add, view, change, and delete.

# using formsets for source modules
formsets manage multiple instances of a certain form

# reordering modules and their contents
HTML Drag and Drop API to use fetch api to send an async http request that stores the new module order

python -m pip install django-braces==1.15.0
django-braces contains a collection of generic mexins that provides additiona features for class-based views that are useful for various common scenarios

# Using cache framework
Django includes a robust cache system that allows you to cache data with different levels of granularity. You can cache a single query, the output of a specific view, parts of rendered template content, or your entire site. Items are stored in the cache system for a default time, but you can specify the timeout when you cache data.

docker pull memcached:1.6.26
docker run -it --rm --name memcached -p 11211:11211 memcached:1.6.26 -m 64
python -m pip install pymemcache==4.0.0

## cache levels that django provides
- Low-level cache API: Provides the highest granularity. Allows you to cache specific queries or calculations.
- Template cache: Allows you to cache template fragments.
- Per-view cache: Provides caching for individual views.
- Per-site cache: The highest-level cache. It caches your entire site.

## redis
python -m pip install django-redisboard==8.4.0

# Building API
Django REST framework
- Serializers: To transform data into a standardized format that other programs can understand, or to deserialize data, by converting data into a format that your program can process.
- Parsers and renderers: To render (or format) serialized data appropriately before it is returned in an HTTP response. Similarly, to parse incoming data to ensure that it’s in the correct form.
- API views: To implement the application logic.
- URLs: To define the API endpoints that will be available.
- Authentication and permissions: To define authentication methods for the API and the permissions required for each view.

## Handling Authentication
DRF provides authentication classes to identify the user performing the request. If authentication is successful, the framework sets the authenticated User object in request.user.
DRF provides the following authentication backends:
- BasicAuthentication
- TokenAuthentication
- SessionAuthentication
- RemoteUserAuthentication

## Adding permissions to views
- AllowAny: Unrestricted access, regardless of whether a user is authenticated or not.
- IsAuthenticated: Allows access to authenticated users only.
- IsAuthenticatedOrReadOnly: Complete access to authenticated users. Anonymous users are only allowed to execute read methods such as GET, HEAD, or OPTIONS.
- DjangoModelPermissions: Permissions tied to django.contrib.auth. The view requires a queryset attribute. Only authenticated users with model permissions assigned are granted permission.
- DjangoObjectPermissions: Django permissions on a per-object basis.


