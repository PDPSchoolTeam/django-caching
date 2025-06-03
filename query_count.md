 **`select_related` bilan** va **`select_related`-siz** Django querysetlarning taqqoslamasini (`query count`) ko‘rsataman. Bu orqali siz N+1 muammo nima ekanligini real misolda ko‘rishingiz mumkin.

---

## 🔬 1. Model tuzilmasi (misol uchun)

```python
# models.py
class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔍 2. Django Debug Panel (`django-debug-toolbar`) bilan kuzatish

### ✅ Variant A: `select_related` bilan

```python
products = Product.objects.select_related('category').all()

for product in products:
    print(product.name, product.category.name)
```

**🟢 Query count:**

```
1. SELECT * FROM product
2. SELECT * FROM category WHERE id IN (...)
```

➡ **Jami: 1 ta JOIN bilan bitta query** yoki maksimal 2ta.

---

### ❌ Variant B: `select_related` **yo‘q**

```python
products = Product.objects.all()

for product in products:
    print(product.name, product.category.name)
```

**🔴 Query count (N+1):**

```
1. SELECT * FROM product
2. SELECT * FROM category WHERE id = 1
3. SELECT * FROM category WHERE id = 2
...
n. SELECT * FROM category WHERE id = n
```

➡ **Jami: 1 (asosiy) + N (category so‘rovlari)**
Masalan: 1 + 20 = **21 so‘rov!**

---

## 📊 Yakuniy Taqqoslama Jadvali

| Holat        | select\_related              | Querylar soni | Tezlik (katta dataset) |
| ------------ | ---------------------------- | ------------- | ---------------------- |
| ✅ Optimal    | `select_related('category')` | 1-2 so‘rov    | Yuqori                 |
| ❌ N+1 muammo | yo‘q                         | 1 + N so‘rov  | Sekinlashadi           |

---

## 💡 Tavsiya

* Kichik datasetlar: `select_related` bo‘lmasa ham bo‘ladi.
* Katta datasetlar yoki sahifalangan ro‘yxatlar: `select_related` **shart**.
* `prefetch_related()` — `ManyToMany` yoki `reverse FK` uchun ishlatiladi.

