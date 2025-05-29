from django import forms
from .models import Order, OrderItem
from inventory.models import Product
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supermarket_name']
        widgets = {
            'supermarket_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        supermarket_name = cleaned_data.get('supermarket_name')
        if not supermarket_name:
            self.add_error('supermarket_name', 'This field is required.')
        if not re.match(r'^[A-Za-z_\s]+$', supermarket_name):
            self.add_error("supermarket_name", "Supermarket name must contain only letters and spaces.")

        return cleaned_data


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order', None)
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        product = cleaned_data.get("product")
        if product and self.order:
            exists = OrderItem.objects.filter(order=self.order, product=product).exists()
            if exists:
                self.add_error("product", "This product is already added to the order.")
        elif not product:
            self.add_error("product", "Please select a product.")
        if quantity is not None and quantity < 1:
            self.add_error("quantity", "Quantity must be at least 1")
        remaning_quantity = product.quantity - quantity
        if remaning_quantity < product.critical_quantity :
            self.add_error("quantity",f"Cannot order this quantity. It would drop below the critical quantity ({product.critical_quantity}).")
        return cleaned_data
