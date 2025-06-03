from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app.models import Address, Product


# @cache_page(60 * 2)  # Ushbu view 2 daqiqaga keshlanadi # noqa
def address_list(requests):
    addresses = Address.objects.all()
    return render(requests, 'home.html', {'addresses': addresses})


def product_list_view(request):
    key = "cached_products"
    products = cache.get(key)

    if products is None:
        products = (
            Product.objects.select_related('category')
            .only('id', 'name', 'price', 'category__name')
            .order_by('-created_at')
        )
        cache.set(key, products, timeout=60 * 10)  # Cache for 10 minutes

    paginator = Paginator(products, 20)  # paginate by 20
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "product_list.html", {"page_obj": page_obj})


def product_detail_view(request, pk):
    key = f"product:{pk}"
    product = cache.get(key)

    if product is None:
        product = get_object_or_404(Product.objects.select_related("category"), id=pk)
        cache.set(key, product, timeout=60 * 15)  # Cache for 15 minutes

    return render(request, "product_detail.html", {"product": product})


# cache ishlatilmagan, ya’ni toza (non-cached) # noqa
# def product_list_view(request):
#     products = (
#         Product.objects.select_related('category')
#         .only('id', 'name', 'price', 'category__name')
#         .order_by('-created_at')
#     )
#
#     paginator = Paginator(products, 20)  # paginate by 20
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, "product_list.html", {"page_obj": page_obj})
#
#
# def product_detail_view(request, pk):
#     product = get_object_or_404(
#         Product.objects.select_related("category"),
#         id=pk
#     )
#     return render(request, "product_detail.html", {"product": product})
#

"""
| Qism                           | Izoh                                                                              |
| ------------------------------ | --------------------------------------------------------------------------------- |
| `cache.get()` va `cache.set()` | Olib tashlandi — har bir request DB'dan ma'lumot olib keladi                      |
| `Paginator`                    | Saqlab qolindi, chunki u katta datasetlar bilan ishlashda optimaldir              |
| `select_related()` va `only()` | DB so‘rovini engillashtirish uchun qolgan — bu hali ham best practice hisoblanadi |
 
"""  # noqa

# N+1 muammo (performance pasayishi) # noqa
"""
Bu holda har bir ForeignKey maydon (masalan, product.category.name) uchun alohida so‘rov (query) yuboriladi.
Bu kichik datasetlarda muammo tug‘dirmaydi, lekin katta datasetlarda N+1 muammo (performance pasayishi) yuzaga keladi.
"""  # noqa
# def product_list_view(request):
#     products = (
#         Product.objects
#         .only('id', 'name', 'price', 'category_id')  # Faqat model fieldlar # noqa
#         .order_by('-created_at')
#     )
#
#     paginator = Paginator(products, 20)  # paginate by 20
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, "product_list.html", {"page_obj": page_obj})
#
#
# def product_detail_view(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     return render(request, "product_detail.html", {"product": product})


"""
E’tibor bering:

.select_related('category') olib tashlangan.
.only(...) ichida category__name emas, category_id yozilgan (bu model fieldi hisoblanadi).
template da siz .category.name deb yozsangiz, u holda har bir mahsulot uchun alohida so‘rov bo‘ladi: SELECT * FROM category WHERE id = ?.

N+1 Muammo Misoli

{% for product in page_obj %}
  {{ product.category.name }}  <!-- Har biri uchun yangi query! -->
{% endfor %}
Agar siz 20 ta product ko‘rsatsangiz, bu 1 ta asosiy query + 20 ta category query bo‘ladi → 21 so‘rov.
"""  # noqa
