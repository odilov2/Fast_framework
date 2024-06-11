from django.contrib import admin
from .models import Products, Order, Category

admin.site.register([Products, Order, Category])

