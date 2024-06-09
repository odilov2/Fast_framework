from django.urls import path
from .views import ProductView, CategoryView, OrderView

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('category/', CategoryView.as_view(), name='category'),
    path('order/', OrderView.as_view(), name='order')
]