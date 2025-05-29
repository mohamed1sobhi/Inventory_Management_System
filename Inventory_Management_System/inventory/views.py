from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product
from orders.models import Order
from shipment.models import Shipment
from django.db.models import Count, F
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib import messages
import pandas as pd 
from itertools import chain
import plotly.express as px
import plotly.offline as pyo

def search_product(request):
    query = request.GET.get("query", "").strip()
    if not query:
        messages.warning(request, "Please enter a product name.")
        return render(request, "inventory/inventory.html", context={"products": [], "query": ""})
    products = Product.objects.filter(name__icontains=query)
    if not products.exists():
        messages.error(request, f"No products found for '{query}'.")
    return render(request, "inventory/inventory.html", context={"products": products, "query": query})

class List_all_products(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'inventory/inventory.html'
    context_object_name = 'products'
    login_url = 'login'
    redirect_field_name = 'next'

class Update_product(LoginRequiredMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('list_all')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Product"
        context["btn_name"] = "Update_product"
        return context

class create_product(LoginRequiredMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('list_all')
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



class Dashboard(LoginRequiredMixin,UserPassesTestMixin, View):
    def get(self, request):
        return render(request, "accounts/dashboard.html")
    def test_func(self):
        return self.request.user.role == "manager"
    def handle_no_permission(self):
        messages.error(self.request,"you have no access to dashboard ")
        return redirect("home")

    def post(self, request, query_name):
        shipment_count = Shipment.objects.count()
        order_count = Order.objects.count()
        product_count = Product.objects.count()

        context = {
            'shipment_count': shipment_count,
            'order_count': order_count,
            'product_count': product_count,
        }

        def create_chart(df, x_col, y_col, title, color):
            """Generates a clean and professional bar chart."""
            fig = px.bar(df, x=x_col, y=y_col, title=title, text=y_col)

            fig.update_traces(
                marker=dict(
                    color=color,
                    line=dict(color='black', width=1),
                    opacity=0.9
                ),
                textfont_size=14,
                # textposition="outside",
                width=0.35  
            )

            fig.update_layout(
                paper_bgcolor="#f8f9fa",  
                plot_bgcolor="white",
                xaxis=dict(title=x_col, tickangle=-30),
                yaxis=dict(title=y_col, gridcolor="lightgray", zerolinecolor="gray"),
                font=dict(family="Arial", size=14, color="black"),
                bargap=0.4,
                margin=dict(l=50, r=50, t=30, b=20),
                showlegend=False
            )

            return pyo.plot(fig, output_type="div")

        # Product Insights Chart (Cool Blue)
        if query_name == 'product':
            products = Product.objects.values("name", "quantity")
            df = pd.DataFrame(list(products))
            if not df.empty:
                context["img"] = create_chart(df, "name", "quantity", "Product Quantity", "#3B82F6")

        # Shipment Insights Chart (Calm Teal)
        elif query_name == 'shipment':
            shipments = Shipment.objects.annotate(
                num_products=Count('shipment_items__product', distinct=True)
            ).values('factory_name', 'num_products')
            df = pd.DataFrame(list(shipments))
            if not df.empty:
                context["img"] = create_chart(df, "factory_name", "num_products", "Products Per Shipment", "#14B8A6")

        # Order Insights Chart (Soft Green)
        elif query_name == 'order':
            orders = Order.objects.annotate(
                num_products=Count('order_items__product', distinct=True)
            ).values('supermarket_name', 'num_products')
            df = pd.DataFrame(list(orders))
            if not df.empty:
                context["img"] = create_chart(df, "supermarket_name", "num_products", "Products Per Order", "#10B981")

        return render(request, "accounts/dashboard.html", context)

def approved_info(request):
    orders = Order.objects.select_related("approved_by").values(
        approved_by_name=F("approved_by__username"),
        name=F("supermarket_name"), 
        type=F("status")
    )
    shipments = Shipment.objects.select_related("approved_by").values(
        approved_by_name=F("approved_by__username"),
        name=F("factory_name"),
        type=F("status") 
    )
    combined_records = list(chain(orders, shipments))
    return render(request, "accounts/dashboard.html", {"records": combined_records})