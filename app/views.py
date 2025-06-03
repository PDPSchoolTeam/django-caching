from django.views.decorators.cache import cache_page
from django.http import HttpResponse


@cache_page(60 * 2)  # Ushbu view 2 daqiqaga keshlanadi # noqa
def index(requests):
    # View logical
    return HttpResponse("<h1> Welcome to Home page! </h1>")
