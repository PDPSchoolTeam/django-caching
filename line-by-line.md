
---

## `product_list_view(request)` – **Mahsulotlar ro‘yxati sahifasi**

```python
key = "cached_products"
```

🔹 **Bu cache kaliti**. Redis yoki default Django cache backendda `cached_products` nomi bilan saqlanadi.

---

```python
products = cache.get(key)
```

🔹 `key` (cached\_products) orqali oldin saqlangan mahsulotlar ro‘yxatini cache’dan olishga urinyapti.
Agar mavjud bo‘lsa — DB so‘rovi qilinmaydi.

---

```python
if products is None:
```

🔹 Agar cache’da **hech nima yo‘q bo‘lsa** (yoki timeout bo‘lgan bo‘lsa), `products` qiymati `None` bo‘ladi.

---

```python
    products = (
        Product.objects.select_related('category')
        .only('id', 'name', 'price', 'category__name')
        .order_by('-created_at')
    )
```

🔹 `Product` modelidan **`category` bilan birga JOIN qilib**, faqat kerakli ustunlarni (`id`, `name`, `price`, `category__name`) tanlab olib, `created_at` bo‘yicha teskari tartibda olish.
`select_related()` → N+1 muammosini oldini oladi.
`only()` → DB dan faqat kerakli maydonlarni olib, so‘rovni tezlashtiradi.

---

```python
    cache.set(key, products, timeout=60 * 10)
```

🔹 Olingan queryset’ni **10 daqiqaga cache’da saqlaydi**. Shunda keyingi so‘rovlar DBga murojaat qilmaydi.

---

```python
paginator = Paginator(products, 20)
```

🔹 Har bir sahifada 20 tadan mahsulot bo‘lishi uchun **pagination obyekt** hosil qilinadi.

---

```python
page_number = request.GET.get("page")
```

🔹 `?page=2` kabi URL query’dan sahifa raqamini oladi.

---

```python
page_obj = paginator.get_page(page_number)
```

🔹 Sahifalash bajariladi: `page_obj` – bu sahifadagi 20 ta product'ni o‘z ichiga oladi.

---

```python
return render(request, "product_list.html", {"page_obj": page_obj})
```

🔹 `product_list.html` template’ga `page_obj` konteks bilan jo‘natiladi.

---

##  `product_detail_view(request, pk)` – **Mahsulot tafsiloti sahifasi**

```python
key = f"product:{pk}"
```

🔹 Har bir product uchun alohida cache key (masalan, `product:5`) yaratadi.

---

```python
product = cache.get(key)
```

🔹 Cache’dan `product:5` ni olib ko‘radi.

---

```python
if product is None:
    product = get_object_or_404(Product.objects.select_related("category"), id=pk)
    cache.set(key, product, timeout=60 * 15)
```

🔹 Agar cache’da bo‘lmasa:

* `Product` modelidan `pk` bo‘yicha `category` bilan birga JOIN qilib DBdan olib keladi.
* Olingan product 15 daqiqaga cache’da saqlanadi.

---

```python
return render(request, "product_detail.html", {"product": product})
```

🔹 Mahsulot ma’lumoti `product_detail.html` template’ga kontekst sifatida jo‘natiladi.

---

##  Umumiy axborot:

| Element            | Maqsad                                                    |
| ------------------ | --------------------------------------------------------- |
| `cache.get()`      | Cache’dan ma’lumot olish                                  |
| `cache.set()`      | Cache’ga ma’lumot qo‘shish                                |
| `select_related()` | JOIN orqali `ForeignKey` modelni bitta query’da olish     |
| `only()`           | Faqat kerakli ustunlarni olish (queryni yengillashtiradi) |
| `Paginator`        | Sahifalash uchun foydalaniladi                            |

---
