
from django.db import models
from accounts.models import User
from inventory.models import Product
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivered', 'Delivered'),
    ]
    supermarket_name = models.CharField(max_length=100, unique = True )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_orders')

    def __str__(self):
        return f"Order {self.id} for {self.supermarket_name}"
    class Meta():
        db_table = 'order'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    class Meta():
        db_table = 'orders_items'
        unique_together = ('order', 'product')

