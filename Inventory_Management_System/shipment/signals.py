from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Shipment
from inventory.models import Product

@receiver(pre_save, sender=Shipment)
def update_inventory_on_delivery(sender, instance, **kwargs):
    # get the previous instance from db
    try:
        previous_instance = Shipment.objects.get(id=instance.id)
    except Shipment.DoesNotExist:
        previous_instance = None

    # check status if "Delivered"
    if previous_instance and previous_instance.status != "Delivered" and instance.status == "Delivered":
        for item in instance.shipment_items.all():
            product_name = item.product.name 
            
            product, created = Product.objects.get_or_create(
                name__iexact=product_name,
                defaults={'quantity': 0} 
            )
            product.quantity += item.quantity
            product.save()
