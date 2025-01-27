from django.shortcuts import render
from testingapp.templates import *
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
# Create your views here.

def main(request):
    context = {}
    return render(request, 'base.html', context)

def store(request):
    all_products = Product.objects.all()
    data = cartData(request)
    cartitems= data['cartitems']

    context = {"products": all_products, 'cartitems':cartitems}
    return render(request, 'store.html', context)

def cart(request):

    data = cartData(request)
    items= data['items']
    order= data['order']
    cartitems= data['cartitems']

    context = {'items':items, 'order':order, 'cartitems':cartitems}
    return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request)
    items= data['items']
    order= data['order']
    cartitems= data['cartitems']

    context = {'items':items, 'order':order, 'cartitems':cartitems}
    return render(request, 'checkout.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = Orderitem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item added", safe=False)

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order =  guestOrder(request, data)  

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
        order.save()

    if order.shipping == True:
        Shippingaddress.objects.create(
            customer = customer,
            order = order,
            address = data['shippinginfo']['address'],
            city = data['shippinginfo']['city'],
            state = data['shippinginfo']['state'],
            zipcode = data['shippinginfo']['zipcode']
        )    

    return JsonResponse('payment done!!', safe=False)