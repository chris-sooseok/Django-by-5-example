# Chapter 4: building social website authentication

## Django auth framework
Login, logout, password change, receovery, etc, features
Django auth framework provides authentiation, sessions, permissions, and user groups models, views, and forms
You can always customize these templates, models, forms if you want

## Middleware
middleware is classes with methods that are globally executed during the request or response phase.

django.contrib.auth comes with two middleware classes found in the setting
- AuthenticationMiddleware: associates users with requests using sessions
- SessionMiddleware: handles the current session across requests

The current user is set in the HttpRequest by the authentication middleware. You can access it with request.user in template files
## form clean method
forms.ModelForm comes with built-in clean method which is called to validate form data when is_valid is called
You can override this method or use clean_<fieldname> to apply it to a specific field

## auth password hashing
PBKDF2 hasher is used by default since scrypt which is more secure requires OpenSSL and more memory

## Extending user model: adding profile


# Chapter 5: Oauth Authentication and profile creation pipeline

## Messages
Messaes are stored in a cookie by default (falling back to session storage), and they are displayed and cleared in the next request from the user.

## Context processor
A context processor is a Python function that takes the request object as an argument and returns a dictionary that gets added to the request context which you can access within template files

## Custom authentication backend
DJango allows you to authentiate users against different sources, such as
- the built-in Django authentication system
- LDAP (Lightweight Directory Acess Protocol) servers
- third-party providers

## AUTHENTICATION BACKENDS
The AUTHENTICATION_BACKENDS setting includes a list of authentication backends available in the project

The default setting is ['django.contrib.auth.backends.ModelBackend'], which authenticates users against the database using the User model
Whenever authenticate() function is called, DJango tries to authenticate the user against each of the backends defined in AUTHENTICATION_BACKENDS one by one

Django provides a simple way to define your own authentication backends. An authentication backend is a class that provides the following two methods
- authenticate(): It takes the request object and user crendentials as parameters. It has to return a user object that matches those credentials if the credentials are valid, or None otherwise. The request parameter is an HttpRequest object, or None if it’s not provided to the authenticate() function.
- get_user(): It takes a user ID parameter and has to return a user object.

## Python SSO (single sign-on) Oauth (open authorization) Steps
1. python -m pip install social-auth-app-django==5.4.0
2. Add app to INSTALLED_APPS and add path to social_django
3. open /etc/hosts file and add 127.0.0.1 mysite.com 
4. include mysite.com in ALLOWED_HOSTS 

The Transport Layer Security (TLS) protocol is the standard for serving websites through a secure connection
The TLS predecessor is the Secure Socekts Layer (SSL)

The Django development server is not able to serve your site through HTTPS since that is not its intended use.
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

## Profile creation pipeline with Oauth

# Chapter 6: Implementing Bookmark

## Bookmarklet implementation
- add bookmarklet_launcher.js to bookmark bars
- launcher will add bookmark DOM
- bookmark DOM display all image elements found on a page
- add click event to each image that clikcing will redirect to bookmark page on your website

## thumbnails using easy-thembnails
- use {% load thumbnail %} to create and display thumbnails of images
- path to upload thumbnail image is specified by MEDIA_ROOT and upload_to field

## Asynchronous Javascript and XML (AJAX) to implment "like" feature
- AJAX is a misleading name because AJAX requests can exchange data not only in XML format but also in formats such as JSON, HTML, and plain text
- send request without reloading - JS fetch function

### JavaScript and Django template
- In some cases, it is useful to generate JavaScript code dynamically using Django in order to use the results of QuerySets or server-side calculations to define variables in JavaScript.
- We have to include the CSRF token in all JS fetch requests that use unsafe HTTP methods, such as POST or PUT.

- To include CSRF token in HTTP requests through JavsScript, we will need to retrieve the token from the csrftoken cookie, which is set by Django if the CSRF protection is active. To handle csrftoken cookie, use JavaScript Cookie which is a lightweight JS API for handling cookies
 
## Infinite scrolling
image list view that handles both standard browser requests and requests originating from JS
render whole page for the first page request, and append only images for additional request that originates from JS


# Chapter 7: Tracking user actions
Building Follow Systems
    - Creating many-to-many relationship between users by using a custom intermediate model
    - Adding or deleting relationship through the intermediate model

## Creating an activity stream application
Contenttype framework
- Can track all models installed in your project and provides a generic interface to interact with your models
- contenttypes app contains a ContentType model of which instances represents the actual models of your application. New instances of ContentType are automatically created when new models are installed in your project
- each model contains fields
    -   app_label, model, and name
    
Generic key
- Generic relations allow you to associate models in a non-exclusive manner, enabling a single model to relate to multiple other models.


