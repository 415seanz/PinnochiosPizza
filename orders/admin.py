from django.contrib import admin

from .models import Category, Size, Item, Addition, Topping, OrderItem, Order

# Register your models here.

admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Item)
admin.site.register(Addition)
admin.site.register(Topping)
admin.site.register(OrderItem)
admin.site.register(Order)
