
---
# Mysite
----

# Chap 2: Basic social features
### Using canonical URLs for models 
A function named, get_absolute_url, to directly route clients to specific urls

### Adding pagination
### Class-based views
Advantages are

    - to organize code related to HTTP methods, such as GET, or POST in separate methods, instead of using conditional branching
    - to use multiple inheritance to create resuable view classes
### Sending emails with Django
### Adding comments to posts using forms from models

## Adding comments to post


# Chap 3: extending your blog application

### taggit for tag implementation
Manage content in a non-hierarchical manner with third party library
python -m pip install django-taggit==5.0.1

### adding sitemap and RSS feed
    sitemap
    - a sitemap is a file that provides search engines with a list of all the important pages on a website, along with their URLs and other relevant information. This helps search engines crawl and index your website more efficiently, potentially leading to faster crawling and indexing of your content. 

    RSS feed
    - An RSS (Really Simple Syndication) feed is an online file that provides updates about a website's content in a standardized, computer-readable format. It essentially acts as a subscription to a website, allowing users to keep track of new posts, articles, or other content without having to manually visit the site.

### ORM (Object Relational Mapper) - database abstraction API
- is a lyaer of abstraction that you can interact with SQL without writing raw SQL
- Django ORM is based on QuerySets, which is a collection of database queries to retrieve objects from your database
- Django Query Sets are lazy
- You can also create a custom manager that equip your needs of queries


### trigram search
DJango provides a powerful search functionality built on top of PostgreSQL full-text search features. <br>
    - Include 'django.contrib.postgres' in INSTALLED_APPS <br>
    - Trigram search feature can be installed by creating an empty migration file and including TrigramExtensions init it 
        - To create an empty migration file
            - python manage.py makemigrations --name=trigram_ext --empty <appname>
            
- Trigram search can be used for

    - Autocomplete suggestions
    - Search-as-you-type
    - Typo-tolerant search
    - Fuzzy matching names, titles, etc.
    
### Dumping existing data
- docker pull postgres:16.2
- docker run --name=blog_db -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=xxxxx -p 5432:5432 -d postgres:16.2
- python manage.py dumpdata --indent=2 --output=mysite_data.json
- change settings on database
- python manage.py migrate
- python manage.py loaddata mysite_data.json

---
# Bookmarks App
----
# Chapter 4: building social website authentication

### Django auth framework
Login, logout, password change, receovery, etc, features
Django auth framework provides authentiation, sessions, permissions, and user groups models, views, and forms
You can always customize these templates, models, forms if you want

### Middleware
middleware is classes with methods that are globally executed during the request or response phase.

django.contrib.auth comes with two middleware classes found in the setting
- AuthenticationMiddleware: associates users with requests using sessions
- SessionMiddleware: handles the current session across requests

The current user is set in the HttpRequest by the authentication middleware. You can access it with request.user in template files

### form clean method
forms.ModelForm comes with built-in clean method which is called to validate form data when is_valid is called
You can override this method or use clean_<fieldname> to apply it to a specific field

### auth password hashing
PBKDF2 hasher is used by default since scrypt which is more secure requires OpenSSL and more memory

### Extending user model: adding profile


# Chapter 5: Oauth Authentication and profile creation pipeline

### Messages
Messaes are stored in a cookie by default (falling back to session storage), and they are displayed and cleared in the next request from the user.

### Context processor
A context processor is a Python function that takes the request object as an argument and returns a dictionary that gets added to the request context which you can access within template files

### Custom authentication backend
DJango allows you to authentiate users against different sources, such as
- the built-in Django authentication system
- LDAP (Lightweight Directory Acess Protocol) servers
- third-party providers

### AUTHENTICATION BACKENDS
    - The AUTHENTICATION_BACKENDS setting includes a list of authentication backends available in the project
    - The default setting is ['django.contrib.auth.backends.ModelBackend'], which authenticates users against the database using the User model.
    - Whenever authenticate() function is called, DJango tries to authenticate the user against each of the backends defined in AUTHENTICATION_BACKENDS one by one

    - Django provides a simple way to define your own authentication backends. An authentication backend is a class that provides the following two methods
        - authenticate(): It takes the request object and user crendentials as parameters.
            It has to return a user object that matches those credentials if the credentials are valid, or None otherwise.
            The request parameter is an HttpRequest object, or None if it’s not provided to the authenticate() function.
        - get_user(): It takes a user ID parameter and has to return a user object.

### Python SSO (single sign-on) Oauth (open authorization) Steps
1. python -m pip install social-auth-app-django==5.4.0
2. Add app to INSTALLED_APPS and add path to social_django
3. open /etc/hosts file and add 127.0.0.1 mysite.com 
4. include mysite.com in ALLOWED_HOSTS 

### TLS and SSL
The Transport Layer Security (TLS) protocol is the standard for serving websites through a secure connection
The TLS predecessor is the Secure Socekts Layer (SSL)

The Django development server is not able to serve your site through HTTPS since that is not its intended use. <br>
To test the social authentication functionality serving the site through HTTPS, use RunServerPlus extension of the package Django Extensions.
This package contains a collection of useful Django tools.

python -m pip install django-exntesions==3.2.3
python -m pip install werkzeug=3.0.2
- this contains a debugger layer required by the RunServerPlus extension of Django Extensions
python -m pip install pyOpenSSL==24.1.0
- this is required to use the SSL/TLS functionality of RunServerPlus

5. include 'django_extensions' in INSTALLED_APPS
6. python manage.py runserver_plus --cert-file cert.crt
Django Extensions will generate a key and  SSL/TLS certificate automatically, then, now you can access your site with https with the certificate

7. include 'social_core.backends.google.GoogleOAuth2' in AUTHENTICATION_BACKENDS

8. create client id and secret

9. expose <a href="{% url "social:begin" "google-oauth2" %}"> to allow Oauth signin

### Profile creation pipeline with Oauth

# Chapter 6: Implementing Bookmark

### Bookmarklet implementation
- add bookmarklet_launcher.js to bookmark bars
- launcher will add bookmark DOM
- bookmark DOM display all image elements found on a page
- add click event to each image that clikcing will redirect to bookmark page on your website

### thumbnails using easy-thembnails
- use {% load thumbnail %} to create and display thumbnails of images
- path to upload thumbnail image is specified by MEDIA_ROOT and upload_to field

### Asynchronous Javascript and XML (AJAX) to implment "like" feature
- AJAX is a misleading name because AJAX requests can exchange data not only in XML format but also in formats such as JSON, HTML, and plain text
- send request without reloading - JS fetch function

### JavaScript and Django template
- In some cases, it is useful to generate JavaScript code dynamically using Django in order to use the results of QuerySets or server-side calculations to define variables in JavaScript.
- We have to include the CSRF token in all JS fetch requests that use unsafe HTTP methods, such as POST or PUT.

- To include CSRF token in HTTP requests through JavsScript, we will need to retrieve the token from the csrftoken cookie, which is set by Django if the CSRF protection is active. To handle csrftoken cookie, use JavaScript Cookie which is a lightweight JS API for handling cookies
 
### Infinite scrolling
image list view that handles both standard browser requests and requests originating from JS
render whole page for the first page request, and append only images for additional request that originates from JS


# Chapter 7: Tracking user actions
### Building Follow Systems
    - Creating many-to-many relationship between users by using a custom intermediate model
    - Adding or deleting relationship through the intermediate model

### activity stream application with contenttype framework
Contenttype framework
- Can track all models installed in your project and provides a generic interface to interact with your models
- contenttypes app contains a ContentType model of which instances represents the actual models of your application. New instances of ContentType are automatically created when new models are installed in your project
- each model contains fields
    -   app_label, model, and name

Craete action model and create_action function that can be usally globally across your project 
    
Generic key
- Generic relations allow you to associate models in a non-exclusive manner, enabling a single model to relate to multiple other models.

### Optimized QuerySet for relationships
select_related and prefetch_related

### Denormalizing images_total_like count field
- Denormalization is a process to make data redundant in a way that it optimizes read performance by coping related data to an object
- A side effect is that it is difficult to keep your denormalized data updated
There are several ways to improve performance that you have to take into account before denormalizing fields. Consider database indexes, query optimization, and caching before starting to denormalize your data.

### Singals to incremenet image_total_likes count
django offers several signals for models located at django.db.models.signals. Some examples are as follows:
- pre_save and post_save that are sent before or after calling the save() method of a model
- pre_delete and post_delete after of before delete() method of a model or querySet
- m2m_changed when many-to-many field on a model is changed

Django signals are synchronous and blocking. Asynchronous taks are done with Celery

### Application configuration classes
Django allows you to specify configuration classes for your apps, which is <appname>Config file.
The application configuration class allows you to store metadata and the configuration for the application, and it provides introspection for the application. 

### debug toolbar
python -m pip install django-debug-toolbar==4.3.0

Consult debug toolbar to identify sql query exeuction time, request/response cycle process, etc.

python manage.py debugsqlshell
- outputs SQL statements for jango ORM queries

### Storing image view counts with Redis
- key/value database that stores everything in memory
- data can be persisted by dumping data to disk or keeping commands to a log
- versatile and supports diverse data structures


---
# online-shop
---

# Chapter 8: Building an online shop

### shopping cart using sessions
- Session data is stored on the server side, and cookies contain the session ID unless you use the cookie-based session engine.
 The session middleware manages the sending and receiving of cookies. 
 The default session engine stores session data in the database, but you can choose other session engines.

- The session middleware makes the current session available in the request object. You can access the current session using request.sessio

- Session Storage types
    - database
    - file-based
    - cached sessions : cached in backend which provides the best performance
        For better performance use a cache-based session engine. Django supports Memcached out of the box and you can find third-party cache backends for Redis and other cache systems.
    - cached database sessions: Session data is stored in a write-through cache and database. Reads only use the database if the data is not already in the cache.
    - cookie-based sessions

## cart context processor
A contextprocessor is a function that takes the request object as an argument and returns a dictionary that gets added to the request context

## Creating asynchronous tasks
### Message queue, broker, and worker
    - message broker manages message queue of which workers consurm from and execute each action from the queue

### Celery
 - Celery is a distributed task queue that can process vast amounts of messages. Celery communicates via messages and requires a message broker to mediate between clients and workers

python -m pip install celery==5.4.0

 - A celery worker is a process that handles bookkeeping features like
    - sending/receiving queue messages
    - registering tasks
    - killing hung tasks
    - tracking status

 - The CELERY_ALWAYS_EAGER setting allows you to execute tasks locally in a synchronous manner instead of sending them to the queue. This is useful for running unit tests or executing the application in your local environment without running Celery.

### rabbitMQ installation
    - docker pull rabbitmq:3.13.1-management
    - docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
    - http://127.0.0.1:15672/

### Monitoring Celery with Flower
    - other tools to monitor the asynchronous tasks that are executed with Celery
    - python -m pip install flower==2.0.1
### adding security to flower
    - celery -A myshop flower --basic-auth=user:pwd


# Chapter 9: Managing payments and orders
### Integrating a payment gateway
Using a payment gateway, you can manage customers' orders and delegate payment processing to a reliable, secure third party. <br>
Stripe provides different products related to payment processing, such as one-off payment, recurring payments, multiparty payments 

python -m pip install stripe==9.3.0

### Using webhookes to receive payment notifications
    - Stripe can push real-time events to our app by using webhooks.
    - A webhook, also called a callback, can be thought of as an event-driven API instead of a request-driven API.
    - Stripe can send an HTTP request to a URL of our application to notify us of successful payments in real time. The notification of these events will be asynchronous, when the event occurs, regardless of our synchronous calls to the Stripe API.
    - You can add webhook endpoint URLs to your Stripe account to receive events. Since we are using webhooks and we don’t have a hosted website accessible through a public URL, we will use the Stripe Command-Line Interface (CLI) to listen to events and forward them to our local environment.

The Stripe CLI is a developer tool that allows you to test and manage your integration with Stripe directly from your shell
We use this command to tell Stripe to listen to events and forward them to our localhost.
stripe listen --forward-to 127.0.0.1:8000/payment/webhook/

### Referencing Stripe payments in orders
Linking Stripe payment id to your Order model to see the payment details in the Stripe dashboard

### exporting orders to CSV files

### Extending admin state with custom views

### Generating PDF invoices dynamically and sending by email asycnronously
python -m pip install WeasyPrint==61.2

collectstatic command copies all static files from your apps into the directory defined in the STATIC_ROOT setting

Create pdf with weasyprint and attach it to email being sent from Celery worker

# Chapter 10: coupons and recommendation systems

### coupon
construct coupon attribute in cart class that is created with session data

### Recommendation System with Redis
Create algorithm logic with Redis by building data whenever items are purchased
Based on the data built, recommend items to each item list

# Chapter 11: Internationalization and localization

### Internalization
Internationalization relies on the GNU gettext toolset to generate and manage message files.
A message file is a plain text file that represents a language. It contains a part, or all, of the translation strings found in your application and their respective translation for a single language. Once the translation is done, message files are compiled to offer rapid access to translated strings

- mekemessages:
    - This runs over the source tree to find all the strings marked for translation and creates or updates the .po message files in the locale directory. A single .po file is created for each language

- compilemessages:
    - This compiles the existing .po message files to .mo files, which are used to retrieve translations.

brew install gettext

brew link --force gettext

### How to add translations to a django project
1. Mark the strings for translation in your Python code and your templates.
2. Run the makemessages command to create or update message files that include all the translation strings from your code.
3. Translate the strings contained in the message files.
4. Compile the message files using the compilemessages management command.

### How dango determines the current language
djnago comes with a middleware that determines the current language based on the request data. This is the LocaleMiddleware that resides in django.middleware.locale.LocaleMiddleware which performs the following tasks
    
    1. If you are using i18n_patterns, that is, you are using translated URL patterns, it looks for a language prefix in the requested URL to determine the current language. You will learn to translate URL patterns in the Translating URL patterns section.
    2. If no language prefix is found, it looks for an existing LANGUAGE_SESSION_KEY in the current user’s session.
    3. If the language is not set in the session, it looks for an existing cookie with the current language. A custom name for this cookie can be provided in the LANGUAGE_COOKIE_NAME setting. By default, the name for this cookie is django_language.
    4. If no cookie is found, it looks for the Accept-Language HTTP header of the request.
    5. If the Accept-Language header does not specify a language, Django uses the language defined in the LANGUAGE_CODE setting.

By default, Django will use the language defined in the LANGUAGE_CODE setting unless you are using LocaleMiddleware. The process described here only applies when using this middleware.

### Translating python code
There are various methods to handle translations within python code
    - Standard translations
    - Lazy translations: Executed when the value is accessed rather than when the function is called.
    A common example where lazy translations are beneficial is in the settings.py file of your project, where immediate translation is not practical because the settings must be defined before the translation system is fully ready.
    - Translations including variables: Used to interpolate variables within strings that are to be translated.
    - Plural forms in translations: Techniques to manage translations that depend on numerical quantities that might affect the string being translated.

For translating literals in your Python code, you can mark strings for translation using the gettext() function included in django.utils.translation. This function translates the message and returns a string. 

django-admin makemessages --all

django-admin compilemessages

### Translating templates
{% translate %} template tag

    - allows you to mark a literal for translation. Internally, exeuctes gettext() on the given text

### Using Rosetta translation interface
Rosetta is a third-party application that allows you to edit translations directly in the browser, using the same interface as the Django administration site. Rosetta makes it easy to edit .po files, and it updates compiled translation files. This eliminates the need to download and upload translation files, and it supports collaborative editing by multiple users.

### URL patterns for internationalization
One reason for translating URLs is to optimize your site for search engines.

### Translating models with django-parler
django-parler generates a separate database table for each model that contains translations. This table includes all the translated fields and a foreign key for the original object that the translation belongs to.

python -m pip install django-parler==2.3

### localization with localflavor which provides localized validation
By default, Django applies the format localization for each locale.

python -m pip install django-localflavor==4.0
    - It’s very useful for validating local regions, local phone numbers, identity card numbers, social security numbers, and so on.

---
Elearning-platform
---


# Chapter 12: building e-learning platform

### building course models
Each course will be divided into a configurable number of modules, and each module will contain a configurable number of contents.

### Using fixtures to provide initial data for models
    - dumpdata: dumps data from db into the standard output. The resulting data structure includes information about the model and its fields for django to be able to load it into db
    - loaddata: load data structure into db

### Creating models for polymorphic content
django offers three options to use model inheritance
- abstract models: Useful when you want to put some common information into several models
- Multi-table model inheritance: In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship between the child model and its parent model
- Proxy models: Useful when you need to change the behavior of a model, for example, by including additional methods, changing the default manager, or using different meta options

### Creating custom model fields
you can also create your own model fields to store custom data or alter the behavior of existing
fields. Custom fields allow you to store unique data types, implement custom validations, encapsulate
complex data logic related to the field, or define specific rendering forms using custom widgets.

# Chapter 13: Creating a content management system

### class-based views
When you need to provide a specific behavior for several class-based views, it is recommended that you use mixins.
Mixins are a type of class designed to supply methods to other classes but aren’t intended to be used independently. This allows you to develop shared functionalities that can be incorporated into various classes in a modular manner, simply by having those classes inherit from mixins. 
The concept is similar to a base class, but you can use multiple mixins to extend the funtionality of a given class

### Working with groups and permissions
By default, Django generates four permissions for each model in the installed applications: add, view, change, and delete.

### using formsets for source modules
formsets manage multiple instances of a certain form

### reordering modules and their contents
HTML Drag and Drop API to use fetch api to send an async http request that stores the new module order

python -m pip install django-braces==1.15.0
django-braces contains a collection of generic mexins that provides additiona features for class-based views that are useful for various common scenarios

### Using cache framework
Django includes a robust cache system that allows you to cache data with different levels of granularity. You can cache a single query, the output of a specific view, parts of rendered template content, or your entire site. Items are stored in the cache system for a default time, but you can specify the timeout when you cache data.

docker pull memcached:1.6.26
docker run -it --rm --name memcached -p 11211:11211 memcached:1.6.26 -m 64
python -m pip install pymemcache==4.0.0

### cache levels that django provides
    - Low-level cache API: Provides the highest granularity. Allows you to cache specific queries or calculations.
    - Template cache: Allows you to cache template fragments.
    - Per-view cache: Provides caching for individual views.
    - Per-site cache: The highest-level cache. It caches your entire site.

### redis
python -m pip install django-redisboard==8.4.0

### Building API
Django REST framework
- Serializers: To transform data into a standardized format that other programs can understand, or to deserialize data, by converting data into a format that your program can process.
- Parsers and renderers: To render (or format) serialized data appropriately before it is returned in an HTTP response. Similarly, to parse incoming data to ensure that it’s in the correct form.
- API views: To implement the application logic.
- URLs: To define the API endpoints that will be available.
- Authentication and permissions: To define authentication methods for the API and the permissions required for each view.

### Handling Authentication
DRF provides authentication classes to identify the user performing the request. If authentication is successful, the framework sets the authenticated User object in request.user.
DRF provides the following authentication backends:
    - BasicAuthentication
    - TokenAuthentication
    - SessionAuthentication
    - RemoteUserAuthentication

### Adding permissions to views
- AllowAny: Unrestricted access, regardless of whether a user is authenticated or not.
- IsAuthenticated: Allows access to authenticated users only.
- IsAuthenticatedOrReadOnly: Complete access to authenticated users. Anonymous users are only allowed to execute read methods such as GET, HEAD, or OPTIONS.
- DjangoModelPermissions: Permissions tied to django.contrib.auth. The view requires a queryset attribute. Only authenticated users with model permissions assigned are granted permission.
- DjangoObjectPermissions: Django permissions on a per-object basis.

## Building chat server

### Asynchronous applications using ASGI
Django is usually deployed using Web Server Gateway Interface (WSGI), which is the standard interface for Python applications to handle HTTP requests.
By using ASGI, we will enable Django to handle each message independently and in real time, creating a smooth and live chat experience for students.

### The request/reponse cycle using Channels
Your existing synchronous views will co-exist with the WebSocket functionality that we will implement with Daphne, and you will serve both HTTP and WebSocket requests.
python -m pip install -U 'channels[daphne]==4.1.0'

### daphne
When daphne is added to the INSTALLED_APPS setting, it takes control over the runserver command, replacing the standard Django development server. This will allow you to serve asynchronous requests during development. Besides handling URL routing to Django views for synchronous requests, Daphne also manages routes to WebSocket consumer

### Consumer
Consumers handle WebSockets in a very similar way to how traditional views handle HTTP requests. Consumers are ASGI applications that can handle messages, notifications, and other things. Unlike Django views, consumers are built for long-running communication. URLs are mapped to consumers through routing classes that allow you to combine and stack consumers.

### Channel layer
Channel layers allow you to communicate between different instances of an application. A channel layer is the transport mechanism that allows multiple consumer instances to communicate with each other and with other parts of Django.

### Channels and groups
Channel layers provide two abstractions to manage communications: channels and groups:
- Channel: You can think of a channel as an inbox where messages can be sent or as a task queue. Each channel has a name. Messages are sent to a channel by anyone who knows the channel name and then given to consumers listening on that channel.
Group: Multiple channels can be grouped into a group. Each group has a name. A channel can be added or removed from a group by anyone who knows the group name. Using the group name, you can also send a message to all channels in the group.

### Redis as a channel layer
python -m pip install channels-redis==4.2.0


### Modifying consumer to be fully asynchronous
Synchronous consumers operate in a way that each request must be processed in sequence, one after
the other. Synchronous consumers are convenient for accessing Django models and calling regular
synchronous I/O functions. However, asynchronous consumers perform better because of their ability
to perform non-blocking operations, moving to another task without waiting for the first operation
to complete. They don’t require additional threads when handling requests, thus reducing wait times
and increasing the ability to scale to more users and requests simultaneously.


## Deployment

docker compose exec web python /code/educa/manage.py migrate

### serving django through WSGI and NGINX
Django’s primary deployment platform is WSGI. WSGI stands for Web Server Gateway Interface , and it is the standard for serving Python applications on the web.
When you generate a new project using the startproject command, Django creates a wsgi.py file inside your project directory. This file contains a WSGI application callable, which is an access point to your application.
WSGI is used for both running your project with the Django development server and deploying your application with the server of your choice in a production environment

### NGINX
NGINX is a web server focused on high concurrency, performance, and low memory usage. NGINX also acts as a reverse proxy, receiving HTTP and WebSocket requests and routing them to different backends.

uWSGI is capable of serving static files flawlessly, but it is not as fast and effective as NGINX

### Collecting static files
Each application in your Django project may contain static files in a static/ directory. Django provides a command to collect static files from all applications into a single location. This simplifies the setup for serving static files in production. The collectstatic command collects the static files from all applications of the project into the path defined with the STATIC_ROOT setting.

### Securing site with SSL/TLS
The TLS protocol is the standard for serving websites through a secure connection. The TLS predecessor is SSL. Although SSL is now deprecated, in multiple libraries and online documentation, you will find references to both the terms TLS and SSL. It’s strongly encouraged that you serve your websites over HTTPS.

### Checking your project for production
python manage.py check --settings=educa.settings.local
python manage.py check --deploy --settings=educa.settings.local

### HTTP Strict Transport Security (HSTS)
The HSTS policy prevents users from bypassing warnings and connecting to a site with an expired, self-signed, or otherwise invalid SSL certificate.
When you own a real domain, you can apply for a trusted Certificate Authority (CA) to issue an SSL/TLS certificate for it, so that browsers can verify its identity. In that case, you can give a value to SECURE_HSTS_SECONDS higher than 0, which is the default value

### inclduing Daphne in the NGINX configuration
NGINX runs in front of uWSGI and Daphne as a reverse proxy server. NGINX faces the web and passes
requests to the application server (uWSGI or Daphne) based on their path prefix. Besides this, NGINX
also serves static files and redirects non-secure requests to secure ones. This setup reduces downtime,
consumes fewer server resources, and provides greater performance and security.

For more advanced production environments, you will need to dynamically distribute containers
across a varying number of machines. For that, instead of Docker Compose, you will need an orches-
trator like Docker Swarm mode or Kubernetes

### Creating a custom middleware

