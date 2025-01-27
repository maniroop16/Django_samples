from .models import *
import json

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
    cartitems = order['get_cart_items']
    for i in cart:
        try:
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

            if product.digital == False:
                order['shipping'] = True
        except:
            # This is to avoid getting the item which is removed from db after user added to cart
            pass
    return {'cartitems':cartitems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        cookiecart = cookieCart(request)
        items = cookiecart['items']
        order = cookiecart['order']
        cartitems = cookiecart['cartitems']

    return {'cartitems':cartitems ,'order':order, 'items':items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    print(items)
    customer, created = Customer.objects.get_or_create(
			customer_email=email,
			)
    customer.customer_name = name
    customer.save()

    order = Order.objects.create(
		customer=customer,
		complete=False,
		)
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderitem = Orderitem.objects.create(
		    product=product,
		    order=order,
	        quantity=item['quantity'],
	    )
    return customer, order

