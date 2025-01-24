from django.shortcuts import render
from testingapp.templates import *
from .models import *
from django.http import JsonResponse
import json
import datetime
# Create your views here.

def main(request):
    context = {}
    return render(request, 'base.html', context)

def store(request):
    all_products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartitems = order['get_cart_items']
    context = {"products": all_products, 'cartitems':cartitems}
    return render(request, 'store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        cart = json.loads(request.COOKIES['cart'])
        print(cart)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartitems = order['get_cart_items']
        for i in cart:
            cartitems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
				'product':{
                    'id':product.id,
                    'product_name':product.product_name,
                    'price':product.price, 
				    'imageURL':product.imageURL
                    },
                'quantity':cart[i]['quantity'],
				'digital':product.digital,
                'individual_item_total':total,
				}
            items.append(item)
    context = {'items':items, 'order':order, 'cartitems':cartitems}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartitems = order['get_cart_items']

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

    else:
        print('User not logged in!!')    

    return JsonResponse('payment done!!', safe=False)