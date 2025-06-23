
# Chapter 4: building social website authentication

Django looks for templates by order of appearance in the INSTALLED_APPS settings

## form clean method
forms.ModelForm comes with built-in clean method which is called to validate form data when is_valid is called
You can override this method or use clean_<fieldname> to apply it to a specific field

## Django auth framework
Django auth framework provides authentiation, sessions, permissions, and user groups models, views, and forms
You can always customize these templates, models, forms if you want

## Middleware
middleware is classes with methods that are globally executed during the request or response phase.

django.contrib.auth comes with two middleware classes found in the setting
- AuthenticationMiddleware: associates users with requests using sessions
- SessionMiddleware: handles the current session across requests

## auth password hasing
PBKDF2 hasher is used by default since scrypt which is more secure requires OpenSSL and more memory