from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextChoices


class Category(models.Model):
    name = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'category'


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    count = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'product'


class OrderStatus(TextChoices):
    PENDING = "PENDING", 'pending'
    TRANSIT = "TRANSIT", 'transit'
    DELIVERED = "DELIVERED", 'delivered'

    # class Meta:
    #     db_table = 'orderstatus'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    class Meta:
        db_table = 'order'


# class User(User):
#     pass



