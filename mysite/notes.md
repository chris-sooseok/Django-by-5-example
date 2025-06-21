
# Django Basics
## Logging
- each HTTP request is logged in the console by the development server

## Server
- To deploy Django in a production environment, you should run it as a WSGI application using a web server, such as Apache, Gunicorn, or uWSGI,
- or as an ASGI application using a server such as Daphne or Uvicorn

## Commands
- django-admin startproject <project name> # to start Django project
- python manage.py shell #Django shell
- python manage.py startapp <appname>
- python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings # you can change settings configuration
- python manage.py migrate # apply all database changes from entire apps


------------------------------------------------------------------------------------------
# About Migrations

1. you have defined or changed your data model 
2. python manage.py makemigrations <appname> 
    - create migration file that summarizes your changes to apply them to database
   - it doesn't simply create your migration file, but it compares your previous existing migration and synchronizes your current changes with the existing model
3. python manage.py sqlmigrate <appname> <migration id>
   - display SQL queries to apply your changes to database

CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            "title" varchar(250) NOT NULL, "slug" varchar(250) NOT NULL, 
            "body" text NOT NULL, "publish" datetime NOT NULL, "created" datetime NOT NULL, 
            "updated" datetime NOT NULL, "status" varchar(2) NOT NULL, 
            "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_post_slug_b95473f2" ON "blog_post" ("slug");
CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
CREATE INDEX "blog_post_publish_bb7600_idx" ON "blog_post" ("publish" DESC);
COMMIT;

- Django generates the table names by combining the application name and the lowercase name of the model (blog_post)
- An index in descending order on the publish column. This is the index we explicitly defined with the indexes option of the model’s Meta class.
- An index on the slug column because SlugField fields imply an index by default.
- An index on the author_id column because ForeignKey fields imply an index by default.

4. python manage.py migrate
   - will apply all changes made

## Creating an empty migration file
python manage.py makemigrations --name=filename --empty blog

------------------------------------------------------------------------------------------
##  ORM (Object Relational Mapper) - database abstraction API
- allows you to interact with database without having to write SQL statements
- maps your models to database tables
- Django ORM is based on QuerySets, which is a collection of database queries to retrieve objects from your database
- Django Query Sets are lazy, which means queries are evaluated when forced
- You can also create a custom manager that equip your needs of queries
- used in templates as well

------------------------------------------------------------------------------------------
# Dumping existing data
- docker pull postgres:16.2
- docker run --name=blog_db -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=xxxxx -p 5432:5432 -d postgres:16.2
- python manage.py dumpdata --indent=2 --output=mysite_data.json
- change settings on database
- python manage.py migrate
- python manage.py loaddata mysite_data.json

------------------------------------------------------------------------------------------
# Things to look into
- ordering of db
- indexing of db

------------------------------------------------------------------------------------------
# sitemap and RSS feed
sitemap
- a sitemap is a file that provides search engines with a list of all the important pages on a website, along with their URLs and other relevant information. This helps search engines crawl and index your website more efficiently, potentially leading to faster crawling and indexing of your content. 

RSS feed
- An RSS (Really Simple Syndication) feed is an online file that provides updates about a website's content in a standardized, computer-readable format. It essentially acts as a subscription to a website, allowing users to keep track of new posts, articles, or other content without having to manually visit the site.

# trigram search
Inspect similarities between words
Search and query based on the similarities
	•	Autocomplete suggestions
	•	Search-as-you-type
	•	Typo-tolerant search
	•	Fuzzy matching names, titles, etc.