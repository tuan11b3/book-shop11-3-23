from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from django.views.generic import ListView
from django.db.models import Q

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

    context = {'items': items,'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def product(request, product_id):
    data = cartData(request)

    cartItems = data['cartItems']
    product = Product.objects.get(id = product_id)
    context = {'product': product,  'cartItems':cartItems}

    return render(request, 'store/product.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, status=0)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0
        orderItem.delete()

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, status=0)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    order.total = order.get_cart_total

    if total == float(order.get_cart_total):
        order.status = 1

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
    return render(request, 'store/feedback.html', context)
# 'store/product.html'

class ProductSearchListView(ListView):
    model = Product
    template_name = 'store/search-product.html'
    # context_object_name = 'products'
    def get_queryset(self):
        data = cartData(self.request)

        cartItems = data['cartItems']
        categories = Category.objects.all()

        query = self.request.GET.get('q')
        print("query: ", query)
        products=Product.objects.filter(Q(name__icontains=query))
        context = {'products':products, 'cartItems': cartItems, 'categories': categories}
        return context
    
def product_search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    query = request.GET.get('q')
    products=Product.objects.filter(Q(name__icontains=query))
    categories = Category.objects.all()
    context = {'products':products, 'cartItems': cartItems, 'categories': categories}
    return render(request, 'store/store.html', context)
