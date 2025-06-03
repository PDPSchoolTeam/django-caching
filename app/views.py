from django.views.decorators.cache import cache_page
from django.shortcuts import render

from app.models import Address


# @cache_page(60 * 2)  # Ushbu view 2 daqiqaga keshlanadi # noqa
def address_list(requests):
    addresses = Address.objects.all()
    return render(requests, 'home.html', {'addresses': addresses})
