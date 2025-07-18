
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

# Building chat server

## Asynchronous applications using ASGI
Django is usually deployed using Web Server Gateway Interface (WSGI), which is the standard interface for Python applications to handle HTTP requests.
By using ASGI, we will enable Django to handle each message independently and in real time, creating a smooth and live chat experience for students.

## The request/reponse cycle using Channels
Your existing synchronous views will co-exist with the WebSocket functionality that we will implement with Daphne, and you will serve both HTTP and WebSocket requests.
python -m pip install -U 'channels[daphne]==4.1.0'

## daphne
When daphne is added to the INSTALLED_APPS setting, it takes control over the runserver command, replacing the standard Django development server. This will allow you to serve asynchronous requests during development. Besides handling URL routing to Django views for synchronous requests, Daphne also manages routes to WebSocket consumer

## Consumer
Consumers handle WebSockets in a very similar way to how traditional views handle HTTP requests. Consumers are ASGI applications that can handle messages, notifications, and other things. Unlike Django views, consumers are built for long-running communication. URLs are mapped to consumers through routing classes that allow you to combine and stack consumers.

## Channel layer
Channel layers allow you to communicate between different instances of an application. A channel layer is the transport mechanism that allows multiple consumer instances to communicate with each other and with other parts of Django.

## Channels and groups
Channel layers provide two abstractions to manage communications: channels and groups:
- Channel: You can think of a channel as an inbox where messages can be sent or as a task queue. Each channel has a name. Messages are sent to a channel by anyone who knows the channel name and then given to consumers listening on that channel.
Group: Multiple channels can be grouped into a group. Each group has a name. A channel can be added or removed from a group by anyone who knows the group name. Using the group name, you can also send a message to all channels in the group.

## Redis as a channel layer
python -m pip install channels-redis==4.2.0


## Modifying consumer to be fully asynchronous
Synchronous consumers operate in a way that each request must be processed in sequence, one after
the other. Synchronous consumers are convenient for accessing Django models and calling regular
synchronous I/O functions. However, asynchronous consumers perform better because of their ability
to perform non-blocking operations, moving to another task without waiting for the first operation
to complete. They don’t require additional threads when handling requests, thus reducing wait times
and increasing the ability to scale to more users and requests simultaneously.


# Deployment

docker compose exec web python /code/educa/manage.py migrate

## serving django through WSGI and NGINX
Django’s primary deployment platform is WSGI. WSGI stands for Web Server Gateway Interface , and it is the standard for serving Python applications on the web.
When you generate a new project using the startproject command, Django creates a wsgi.py file inside your project directory. This file contains a WSGI application callable, which is an access point to your application.
WSGI is used for both running your project with the Django development server and deploying your application with the server of your choice in a production environment

## NGINX
NGINX is a web server focused on high concurrency, performance, and low memory usage. NGINX also acts as a reverse proxy, receiving HTTP and WebSocket requests and routing them to different backends.

uWSGI is capable of serving static files flawlessly, but it is not as fast and effective as NGINX

## Collecting static files
Each application in your Django project may contain static files in a static/ directory. Django provides a command to collect static files from all applications into a single location. This simplifies the setup for serving static files in production. The collectstatic command collects the static files from all applications of the project into the path defined with the STATIC_ROOT setting.

## Securing site with SSL/TLS
The TLS protocol is the standard for serving websites through a secure connection. The TLS predecessor is SSL. Although SSL is now deprecated, in multiple libraries and online documentation, you will find references to both the terms TLS and SSL. It’s strongly encouraged that you serve your websites over HTTPS.

## Checking your project for production
python manage.py check --settings=educa.settings.local
python manage.py check --deploy --settings=educa.settings.local

### HTTP Strict Transport Security (HSTS)
The HSTS policy prevents users from bypassing warnings and connecting to a site with an expired, self-signed, or otherwise invalid SSL certificate.
When you own a real domain, you can apply for a trusted Certificate Authority (CA) to issue an SSL/TLS certificate for it, so that browsers can verify its identity. In that case, you can give a value to SECURE_HSTS_SECONDS higher than 0, which is the default value

## inclduing Daphne in the NGINX configuration
NGINX runs in front of uWSGI and Daphne as a reverse proxy server. NGINX faces the web and passes
requests to the application server (uWSGI or Daphne) based on their path prefix. Besides this, NGINX
also serves static files and redirects non-secure requests to secure ones. This setup reduces downtime,
consumes fewer server resources, and provides greater performance and security.

For more advanced production environments, you will need to dynamically distribute containers
across a varying number of machines. For that, instead of Docker Compose, you will need an orches-
trator like Docker Swarm mode or Kubernetes

## Creating a custom middleware
