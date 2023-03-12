from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from . utils import cookieCart, cartData, guestOrder
from .forms import FeedbackForm


# Create your views here.

def collection(request, collection_id):
    "Show all product at category = collection_id"
    # category = Category.objects.get(id = collection_id)
    # products = category.product.all()
    data = cartData(request)

    cartItems = data['cartItems']

    categories = Category.objects.all()
    products = Product.objects.filter(category = collection_id)

    context = {'products': products, 'cartItems': cartItems, 'categories': categories}

    return render(request, 'store/collection.html', context)

def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products':products, 'cartItems': cartItems, 'categories': categories}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def product(request, product_id):

    product = Product.objects.get(id = product_id)
    context = {'product': product}

    return render(request, 'store/product.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.total = order.get_cart_total

    if total == float(order.get_cart_total):
        order.complete = True

    order.save()

    if order.shipping == True:
        sh_add = ShippingAddress(
            # customer=customer,
            # order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            province=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        sh_add.save()
        order.shippingaddress = sh_add
        order.save()

        DSDCKM.objects.create(cus_id = customer, add_id = sh_add)
    return JsonResponse('Payment completed', safe=False)

def feedback_form(request):
    if request.method != 'POST':
        form = FeedbackForm()
    else:
        form = FeedbackForm(request.POST)

        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.custom_id = Customer.objects.get(user = request.user)
            new_feedback.save()
            return render(request, 'store/thanks.html')

    context = {'form': form}
    return render(request, 'store/feedback_form.html', context)
'store/product.html'