from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

User = settings.AUTH_USER_MODEL


class Staff(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    cmnd = models.CharField(max_length=12, blank=False, null=False, unique=True)
    address = models.CharField(max_length=511, blank=False, null=False)
    salary = models.DecimalField(max_digits=11, decimal_places=2)
    date_joined = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=255, null=True, unique=True)
    phone = PhoneNumberField(null=True, blank=False)

    def __str__(self):
        return str(self.name)

class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default =1)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.CharField(max_length=50, null=True)
    num_page = models.IntegerField(default = 0)
    sold = models.IntegerField(default = 0 )
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.CharField(max_length=511, null=True, blank=True)
    images = models.ImageField(null=True, blank=True)
    arthur = models.CharField(max_length=127, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url

class ShippingAddress(models.Model):
    #customer = models.ForeignKey(Customer,  on_delete=models.SET_NULL, blank=True, null = True)
    #order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null = True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

class DSDCKM(models.Model):
    cus_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    add_id = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cus_id', 'add_id')


class Order(models.Model):
    status_name = ((0, 'Unpaid'), (1, 'Paid'), (2, 'Unshipped'), (3, 'Shipped'), (4, 'Complete'))

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    #complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.IntegerField(choices=status_name, default=0, blank=True, null=True)
    shippingaddress = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.FloatField(default = 0)
    #phone_num = models.CharField(max_length=10, null=True, blank=True)
    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems  = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        price = self.product.price
        if self.product.discount > 0.00:
            price = self.product.discount
        total = price * self.quantity
        return total

class Feedback(models.Model):
    custom_id = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False)
    details = models.TextField()
    happy = models.BooleanField()
    responded = models.BooleanField(blank=True, null=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

