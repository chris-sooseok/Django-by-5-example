# Django Basics
## Logging
- each HTTP request is logged in the console by the development server

## Server
- To deploy Django in a production environment, you should run it as a WSGI application using a web server, such as Apache, Gunicorn, or uWSGI,
- or as an ASGI application using a server such as Daphne or Uvicorn



# Chap 2: enhancing blog and adding social features
- create SEO-friendly URLs
- adding pagination
- recommendation by email
- class-based views, ModelForm, 

##  ORM (Object Relational Mapper) - database abstraction API
- allows you to interact with database without having to write SQL statements
- maps your models to database tables
- Django ORM is based on QuerySets, which is a collection of database queries to retrieve objects from your database
- Django Query Sets are lazy, which means queries are evaluated when forced
- You can also create a custom manager that equip your needs of queries
- used in templates as well



# Chap 3: extending your blog application
- taggit for tag implementation
- search queries by similarity
- create custom template tags and filters
- adding sitemap and RSS feed
- using fixtures to dump and load data into db

## sitemap and RSS feed
sitemap
- a sitemap is a file that provides search engines with a list of all the important pages on a website, along with their URLs and other relevant information. This helps search engines crawl and index your website more efficiently, potentially leading to faster crawling and indexing of your content. 

RSS feed
- An RSS (Really Simple Syndication) feed is an online file that provides updates about a website's content in a standardized, computer-readable format. It essentially acts as a subscription to a website, allowing users to keep track of new posts, articles, or other content without having to manually visit the site.

## trigram search
Inspect similarities between words
Search and query based on the similarities
    •    Autocomplete suggestions
    •    Search-as-you-type
    •    Typo-tolerant search
    •    Fuzzy matching names, titles, etc.
    
## Dumping existing data
- docker pull postgres:16.2
- docker run --name=blog_db -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=xxxxx -p 5432:5432 -d postgres:16.2
- python manage.py dumpdata --indent=2 --output=mysite_data.json
- change settings on database
- python manage.py migrate
- python manage.py loaddata mysite_data.json




# Chap 4: building a social website
- authentication features
- custom profile model
- configuration for media file uploads
