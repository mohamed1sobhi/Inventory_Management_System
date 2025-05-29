from django import forms 
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta():
        model = Product
        fields = "__all__"
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        quantity = cleaned_data.get("quantity")
        critical_quantity = cleaned_data.get("critical_quantity")
        if not name:
            self.add_error('name', "Name is required.")
        elif name.isdigit():
            self.add_error('name', "Name cannot be entirely numeric.")

        if description and len(description) > 100:
            self.add_error('description', "Description must be less than 100 characters.")

        if quantity is None or quantity < critical_quantity:
            self.add_error('quantity', "Quantity must be greater than critical_quantity.")

        if critical_quantity is None or critical_quantity < 10:
            self.add_error('critical_quantity', "Critical quantity must be at least 10.")
        return cleaned_data
    