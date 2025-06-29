from celery import shared_task
from django.core.mail import send_mail
from .models import Order


# ! Celery task is just a python function decorated with shared_task
@shared_task
def order_created(order_id):
    """
    Task to send an email notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name}, \n\n'
        f'Your order has been created.\n\n'
        f'Your order ID: {order.id}\n\n'
    )
    mail_sent = send_mail(
        subject,  message, 'admin@shop.com', [order.email]
    )
    return mail_sent