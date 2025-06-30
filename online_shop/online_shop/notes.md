
# Chapter 8: Building an online shop

## shopping cart using sessions
Session data is stored on the server side, and cookies contain the session ID unless you use the cookie-based session engine. The session middleware manages the sending and receiving of cookies. The default session engine stores session data in the database, but you can choose other session engines.

The session middleware makes the current session available in the request object. You can access the current session using request.sessio

Session Storage types
- database
- file-based
- cached sessions : cached in backend which provides the best performance
    For better performance use a cache-based session engine. Django supports Memcached out of the box and you can find third-party cache backends for Redis and other cache systems.
- cached database sessions: Session data is stored in a write-through cache and database. Reads only use the database if the data is not already in the cache.
- cookie-based sessions

## cart context processor
A contextprocessor is a function that takes the request object as an argument and returns a dictionary that gets added to the request context

## Creating asynchronous tasks
Message queue, broker, and worker
- message broker manages message queue of which workers consurm from and execute each action from the queue

### Celery
Celery is a distributed task queue that can process vast amounts of messages. Celery communicates via messages and requires a message broker to mediate between clients and workers

python -m pip install celery==5.4.0

A celery worker is a process that handles bookkeeping features like
- sending/receiving queue messages
- registering tasks
- killing hung tasks
- tracking status

The CELERY_ALWAYS_EAGER setting allows you to execute tasks locally in a synchronous manner instead of sending them to the queue. This is useful for running unit tests or executing the application in your local environment without running Celery.

### rabbitMQ installation
docker pull rabbitmq:3.13.1-management
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
http://127.0.0.1:15672/

### Monitoring Celery with Flower
other tools to monitor the asynchronous tasks that are executed with Celery
python -m pip install flower==2.0.1
### adding security to flower
celery -A myshop flower --basic-auth=user:pwd


# Chapter 9: Managing payments and orders
## Integrating a payment gateway
Using a payment gateway, you can manage customers' orders and delegate payment processing to a reliable, secure third party.
Stripe provides different products related to payment processing, such as one-off payment, recurring payments, multiparty payments 

python -m pip install stripe==9.3.0

## Using webhookes to receive payment notifications
Stripe can push real-time events to our app by using webhooks.
A webhook, also called a callback, can be thought of as an event-driven API instead of a request-driven API.
Stripe can send an HTTP request to a URL of our application to notify us of successful payments in real time. The notification of these events will be asynchronous, when the event occurs, regardless of our synchronous calls to the Stripe API.
You can add webhook endpoint URLs to your Stripe account to receive events. Since we are using webhooks and we don’t have a hosted website accessible through a public URL, we will use the Stripe Command-Line Interface (CLI) to listen to events and forward them to our local environment.

The Stripe CLI is a developer tool that allows you to test and manage your integration with Stripe directly from your shell
We use this command to tell Stripe to listen to events and forward them to our localhost.
stripe listen --forward-to 127.0.0.1:8000/payment/webhook/

## Referencing Stripe payments in orders
Linking Stripe payment id to your Order model to see the payment details in the Stripe dashboard

## exporting orders to CSV files

## Extending admin state with custom views

## Generating PDF invoices dynamically and sending by email asycnronously
python -m pip install WeasyPrint==61.2

collectstatic command copies all static files from your apps into the directory defined in the STATIC_ROOT setting

Create pdf with weasyprint and attach it to email being sent from Celery worker

# Chapter 10: coupons and recomendation systems

## coupon
construct coupon attribute in cart class that is created with session data

## Recommendation System with Redis
Create algorithm logic with Redis by building data whenever items are purchased
Based on the data built, recommend items to each item list

# Chapter 11: Internationalization

Internationalization relies on the GNU gettext toolset to generate and manage message files.
A message file is a plain text file that represents a language. It contains a part, or all, of the translation strings found in your application and their respective translation for a single language. Once the translation is done, message files are compiled to offer rapid access to translated strings

mekemessages: This runs over the source tree to find all the strings marked for translation and creates or updates the .po message files in the locale directory. A single .po file is created for each language

compilemessages: This compiles the existing .po message files to .mo files, which are used to retrieve translations.

brew install gettext
brew link --force gettext

## How to add translations to a django project
1. Mark the strings for translation in your Python code and your templates.
2. Run the makemessages command to create or update message files that include all the translation strings from your code.
3. Translate the strings contained in the message files.
4. Compile the message files using the compilemessages management command.

## How dango determines the current language
djnago comes with a middleware that determines the current language based on the request data. This is the LocaleMiddleware that resides in django.middleware.locale.LocaleMiddleware which performs the following tasks
    
    1. If you are using i18n_patterns, that is, you are using translated URL patterns, it looks for a language prefix in the requested URL to determine the current language. You will learn to translate URL patterns in the Translating URL patterns section.
    2. If no language prefix is found, it looks for an existing LANGUAGE_SESSION_KEY in the current user’s session.
    3. If the language is not set in the session, it looks for an existing cookie with the current language. A custom name for this cookie can be provided in the LANGUAGE_COOKIE_NAME setting. By default, the name for this cookie is django_language.
    4. If no cookie is found, it looks for the Accept-Language HTTP header of the request.
    5. If the Accept-Language header does not specify a language, Django uses the language defined in the LANGUAGE_CODE setting.

By default, Django will use the language defined in the LANGUAGE_CODE setting unless you are using LocaleMiddleware. The process described here only applies when using this middleware.

## Translating python code
There are various methods to handle translations within python code
- Standard translations
- Lazy translations: Executed when the value is accessed rather than when the function is called.
A common example where lazy translations are beneficial is in the settings.py file of your project, where immediate translation is not practical because the settings must be defined before the translation system is fully ready.
- Translations including variables: Used to interpolate variables within strings that are to be translated.
- Plural forms in translations: Techniques to manage translations that depend on numerical quantities that might affect the string being translated.

For translating literals in your Python code, you can mark strings for translation using the gettext() function included in django.utils.translation. This function translates the message and returns a string. 

django-admin makemessages --all
django-admin compilemessages

## Translating templates
{% translate %} template tag
- allows you to mark a literal for translation. Internally, exeuctes gettext() on the given text

## Using Rosetta translation interface
Rosetta is a third-party application that allows you to edit translations directly in the browser, using the same interface as the Django administration site. Rosetta makes it easy to edit .po files, and it updates compiled translation files. This eliminates the need to download and upload translation files, and it supports collaborative editing by multiple users.

## URL patterns for internationalization
One reason for translating URLs is to optimize your site for search engines.

## Translating models with django-parler
django-parler generates a separate database table for each model that contains translations. This table includes all the translated fields and a foreign key for the original object that the translation belongs to.

python -m pip install django-parler==2.3

## localization
By default, Django applies the format localization for each locale.

python -m pip install django-localflavor==4.0
It’s very useful for validating local regions, local phone numbers, identity card numbers, social security numbers, and so on.
