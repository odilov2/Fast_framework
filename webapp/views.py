from django.shortcuts import render
from django.views import View
from .models import Product, Category, Order


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products.html', {'products': products})


class CategoryView(View):
    def get(self, request):
        category = Category.objects.all()
        return render(request, 'category.html', {'category': category})


class OrderView(View):
    def get(self, request):
        order = Order.objects.all()
        return render(request, 'order.html', {'order': order})



