from django.urls import path
from rest_api.views import ProductsView

urlpatterns = [
    path('products/', ProductsView.as_view(), name='products'),
]