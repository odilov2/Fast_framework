from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextChoices


class Category(models.Model):
    name = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'category'


# class Product(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     price = models.FloatField()
#     count = models.PositiveIntegerField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     create_date = models.DateField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'product'


class OrderStatus(TextChoices):
    PENDING = "PENDING", 'pending'
    TRANSIT = "TRANSIT", 'transit'
    DELIVERED = "DELIVERED", 'delivered'

    # class Meta:
    #     db_table = 'orderstatus'


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(verbose_name="Product Name", max_length=50)
    photo = models.CharField(verbose_name="Photo", null=True, max_length=20)
    price = models.FloatField()
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    category_code = models.CharField(verbose_name="Category Code", max_length=10)
    category_name = models.CharField(verbose_name="Category Name", max_length=50)
    subcategory_code = models.CharField(verbose_name="Subcategory Code", max_length=20)
    subcategory_name = models.CharField(verbose_name="Subcategory", max_length=20)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return f"{self.product_name}"


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    class Meta:
        db_table = 'order'


# class User(User):
#     pass


class Users(models.Model):
    full_name = models.CharField(verbose_name="Full Name", max_length=100, null=True, blank=True)
    username = models.CharField(verbose_name="Username", max_length=50, null=True, unique=True)
    telegram_id = models.PositiveBigIntegerField(verbose_name="Telegram ID", unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return {self.full_name, self.username}




