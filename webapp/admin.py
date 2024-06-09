from django.contrib import admin
from .models import Product, Order, Category

admin.site.register([Product, Order, Category])

