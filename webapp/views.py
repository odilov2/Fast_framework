from django.shortcuts import render
from django.views import View
from .models import Products, Category, Order


class ProductView(View):
    def get(self, request):
        products = Products.objects.all()
        return render(request, 'products.html', {'products': products})


class CategoryView(View):
    def get(self, request):
        category = Category.objects.all()
        return render(request, 'category.html', {'category': category})


class OrderView(View):
    def get(self, request):
        order = Order.objects.all()
        return render(request, 'order.html', {'order': order})



