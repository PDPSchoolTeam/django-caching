from django.urls import path
from app.views import address_list

urlpatterns = [
    path('addresses/', address_list, name='address_list'),
]
