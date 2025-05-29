from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True)
    quantity = models.PositiveIntegerField(default=10)
    critical_quantity = models.PositiveIntegerField(default=10, validators=[MinValueValidator(10),MaxValueValidator(30)])

    def is_critical(self):
        return self.quantity == self.critical_quantity

    def __str__(self):
        return self.name
    class Meta():
        db_table = "product"


