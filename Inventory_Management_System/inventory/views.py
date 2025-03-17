from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib import messages
import pandas as pd 
import plotly
import plotly.express as px
import json
import plotly.offline as pyo

#in home page
def search_product(request):
    query = request.GET.get("query")
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request,"inventory/inventory.html",context={"products":products,"query":query})



def home_page(request):
    return render(request,"inventory/inventory.html")

class List_all_products(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'inventory/inventory.html'
    context_object_name = 'products'


class Update_product(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('inventory')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Product"
        context["btn_name"] = "Update_product"
        return context

class create_product(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('inventory')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add Product"
        context["btn_name"] = "Add_product"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Product created successfully!")
        return response

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].widget.attrs.update({'autofocus': 'autofocus'})
        return form

class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, "accounts/dashboard.html")
    def post(self, request, query_name):
        if query_name == 'product':
            products = Product.objects.values("name", "quantity")
            df = pd.DataFrame(list(products))
            fig = px.bar(df, y="quantity", x="name", title="Product Quantity", text="quantity")
            fig.update_layout(paper_bgcolor="yellow", plot_bgcolor="yellow")
            image = pyo.plot(fig, output_type="div")
        elif query_name == 'shipment':
            pass
        elif query_name == 'order':
            pass
        else:
            pass
        return render(request, "accounts/dashboard.html", {"img": image })



#in add_order page
class Create_order():
    pass
#in add_shipment page
class Create_shipment():
    pass
#in add_order page
class Update_order():
    pass
#in add_shipment page
class Update_shipment():
    pass
#in orders page
class Get_all_orders():
    pass
#in shipments page
class Get_all_shipments():
    pass
#in details page
class Order_detalis():
    pass
class Shipment_detalis():
    pass
# in sinup page
class Create_user():
    pass
#in manager page
class Approve_order():
    pass
class Approve_shipment():
    pass
#in marked_products page
class Show_marked_products():
    pass

class Filter():
    pass
# Create your views here.

