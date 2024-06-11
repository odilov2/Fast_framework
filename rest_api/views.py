from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_api.serialisers import ProductsSerializer
from webapp.models import Products


class ProductsView(APIView):
    def get(self, request):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)

        return Response(serializer.data)
