from webapp.models import Products, Users
from rest_framework import serializers


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

