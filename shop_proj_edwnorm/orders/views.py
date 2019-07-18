from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from basket.basket import Basket
from .tasks import order_created


def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            basket.clear()
            
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'basket': basket, 'form': form})
