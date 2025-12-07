import re
from django import forms
from django.forms import inlineformset_factory
from .models import Shipment, ShipmentItem, Product


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['factory_name']
        widgets = {
            'factory_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Factory Name'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        factory_name = cleaned_data.get('factory_name')
        if not factory_name:
            self.add_error('factory_name', 'This field is required.')
        if not re.match(r'^[A-Za-z_\s]+$', factory_name):
            self.add_error("factory_name", "Factory name must contain only letters and spaces.")
        return cleaned_data

class ShipmentItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        self.shipment = kwargs.pop('shipment', None)
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        product = cleaned_data.get("product")
        if product and self.shipment:
            exists = ShipmentItem.objects.filter(shipment=self.shipment, product=product).exists()
            if exists:
                self.add_error("product", "This product is already added to the shipment.")
        elif not product:
            self.add_error("product", "Please select a product.")
        if quantity is not None and quantity < 1:
            self.add_error("quantity", "Quantity must be at least 1")
        return cleaned_data



































# class ShipmentForm(forms.ModelForm):
#     class Meta:
#         model = Shipment
#         fields = ['factory_name', 'status']
#         widgets = {
#             'status': forms.Select(choices=Shipment.STATUS_CHOICES)
#         }

# class ShipmentItemForm(forms.ModelForm):
#     class Meta:
#         model = ShipmentItem
#         fields = ['product', 'quantity']
#         widgets = {
#             'product': forms.Select(),
#         }

# ShipmentItemFormSet = forms.inlineformset_factory(
#     Shipment, ShipmentItem, 
#     form=ShipmentItemForm, 
#     extra=0,
#     can_delete=False    
# )


# UpdateShipmentItemFormSet = forms.inlineformset_factory(
#     Shipment, ShipmentItem, 
#     form=ShipmentItemForm, 
#     extra=0,
#     can_delete=True  
# )
# ShipmentItemFormSet.empty_permitted = False 