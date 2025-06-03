from django.urls import path
from app.views import address_list, product_list_view, product_detail_view

urlpatterns = [
    path('addresses/', address_list, name='address_list'),
    path('', product_list_view, name='product-list'),
    path('product/<int:pk>/', product_detail_view, name='product-detail'),
]
