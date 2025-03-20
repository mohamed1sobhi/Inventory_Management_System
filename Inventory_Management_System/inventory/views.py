from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


#in home page
def search_product(request):
    query = request.GET.get("query")
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request,"inventory/home.html",context={"products":products,"query":query})

def home_page(request):
    return render(request,"inventory/home.html")

class List_all_products(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/home.html'
    context_object_name = 'products'
    login_url = 'login'
    redirect_field_name = 'next'


class Update_product(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Product"
        context["btn_name"] = "Update_product"
        return context

class create_product(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/add_product.html'
    success_url = reverse_lazy('home')
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

