
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
