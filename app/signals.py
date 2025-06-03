from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from app.models import Product


# Agar ma'lumotlar o‘zgaradigan bo‘lsa, siz cache ni tozalashingiz kerak # noqa
@receiver([post_save, post_delete], sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete("cached_products")
    cache.delete(f"product:{instance.id}")
