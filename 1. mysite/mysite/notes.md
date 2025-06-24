# Chap 2: Basic social features
## Using canonical URLs for models
A function named, get_absolute_url, to directly route clients to specific urls

## Adding pagination

## Class-based views
Advantages are
- to organize code related to HTTP methods, such as GET, or POST in separate methods, instead of using conditional branching
- to use multiple inheritance to create resuable view classes

- Sending emails with Django
- Adding comments to posts using forms from models

## Adding comments to post


# Chap 3: extending your blog application

## taggit for tag implementation
Manage content in a non-hierarchical manner with third party library
python -m pip install django-taggit==5.0.1

## adding sitemap and RSS feed
sitemap
- a sitemap is a file that provides search engines with a list of all the important pages on a website, along with their URLs and other relevant information. This helps search engines crawl and index your website more efficiently, potentially leading to faster crawling and indexing of your content. 

RSS feed
- An RSS (Really Simple Syndication) feed is an online file that provides updates about a website's content in a standardized, computer-readable format. It essentially acts as a subscription to a website, allowing users to keep track of new posts, articles, or other content without having to manually visit the site.

## ORM (Object Relational Mapper) - database abstraction API
- is a lyaer of abstraction that you can interact with SQL without writing raw SQL
- Django ORM is based on QuerySets, which is a collection of database queries to retrieve objects from your database
- Django Query Sets are lazy
- You can also create a custom manager that equip your needs of queries


## trigram search
DJango provides a powerful search functionality built on top of PostgreSQL full-text search features.
Include 'django.contrib.postgres' in INSTALLED_APPS
Trigram search feature can be installed by creating an empty migration file and including TrigramExtensions init it 
To create an empty migration file
python manage.py makemigrations --name=trigram_ext --empty <appname>
Trigram search can be used for
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

