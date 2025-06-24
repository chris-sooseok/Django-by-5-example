# Django Logistics

## Basics
Django looks for templates by order of appearance in the INSTALLED_APPS settings

## Logging
- each HTTP request is logged in the console by the development server

## Server
- To deploy Django in a production environment, you should run it as a WSGI application using a web server, such as Apache, Gunicorn, or uWSGI,
- or as an ASGI application using a server such as Daphne or Uvicorn


# Commands

## Basics
- django-admin startproject <project name> # to start Django project
- python manage.py shell #Django shell
- python manage.py startapp <appname>
- python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings # you can change settings configuration

## DB
python manage.py makemigrations <appname> 
    - create migration file that summarizes your changes to apply them to database
    - it doesn't simply create your migration file, but it compares your previous existing migration and synchronizes your current changes with the existing model

python manage.py sqlmigrate <appname> <migration id>
   - display SQL queries to apply your changes to database

python manage.py migrate
   - will apply all changes made


### Creating an empty migration file
python manage.py makemigrations --name=filename --empty blog

