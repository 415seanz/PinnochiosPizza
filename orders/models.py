from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class Size(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name}"

class Item(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    maxToppings = models.IntegerField(blank=True, null=True)
    basePrice = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.category}: {self.name} ({self.size})"

class Addition(models.Model):
    name = models.CharField(max_length=32)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    additionPrice = models.DecimalField(max_digits=6, decimal_places=2)


    def __str__(self):
        return f"{self.name}"

class Topping(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    additions = models.ManyToManyField(Addition, blank=True, related_name="orderitems")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="orderitems")
    orderItemPrice = models.DecimalField(max_digits=4, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.item}: ({self.orderItemPrice})"

class Order(models.Model):
    products = models.ManyToManyField(OrderItem, blank=True, related_name="orders")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.category}: ({self.name})"
