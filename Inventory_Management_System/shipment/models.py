
from django.db import models
from accounts.models import User
from inventory.models import Product

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivered', 'Delivered'),
    ]
    factory_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_shipments')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_shipments')

    def __str__(self):
        return f"Shipment {self.id} from {self.factory_name}"
    class Meta():
        db_table = "shipment"

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL,null=True, related_name='shipment_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    class Meta():
        db_table = "shipment_item"


