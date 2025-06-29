from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem
from .tasks import order_created
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            # ! launch asynchronous (delay) task
            # ! the task will be added to the message queue and executed by the Celery worker asap
            order_created.delay(order.id)

            return render(
                request, 'orders/order/created.html', {'order': order}
            )
    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )
