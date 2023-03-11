from django.contrib import admin
from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.store, name = 'store'),
    path('collection/<int:collection_id>/', views.collection, name = 'collection'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('product/', views.product, name = 'product'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order")
]