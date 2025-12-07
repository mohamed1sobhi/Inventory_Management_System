from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, FormView, DetailView
from django.urls import reverse_lazy
from django.db.models import F
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from inventory.models import Product
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages as message

class OrderCreateView(LoginRequiredMixin,CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'
    success_url = reverse_lazy('orders:order_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add New Oreder"
        context["btn_name"] = "Add Order"
        return context
    def form_valid(self, form):
        pending_order = Order.objects.filter(created_by=self.request.user, status="Pending").exists()
        if pending_order:
            message.error(self.request, "You already have a pending order. Please complete it before creating a new one.")
            return self.form_invalid(form)
        form.instance.created_by = self.request.user
        message.success(self.request, "Order created successfully.")
        return super().form_valid(form)
    
class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    def get_queryset(self):
        return Order.objects.all().order_by('id') 


class OrderDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Order
    template_name = "orders/confirm.html"
    success_url = reverse_lazy("orders:create_order")
    def test_func(self):
        return self.request.user.role == 'manager'
    def handle_no_permission(self):
        message.error(self.request,"only manager can delete order")
        return redirect("orders:order_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordername"] = self.object.supermarket_name if self.object else ''
        return context

class OrderItemCreateView(LoginRequiredMixin,FormView):
    template_name = 'orders/create_order.html'  
    form_class = OrderItemForm
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Add New Item"
        context["btn_name"] = "Add Item"
        return context
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        order_id = self.kwargs.get("order_id")
        print(self.kwargs)
        kwargs["order"] = get_object_or_404(Order,id = order_id)
        return kwargs
    def form_valid(self, form):
        order = self.get_form_kwargs()["order"]
        form.instance.order = order
        form.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))   
    success_url = reverse_lazy("orders:order_list")

class OrderDetailView(LoginRequiredMixin,DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.order_items.all()
        return context

class OrderUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'orders/create_order.html'
    def test_func(self):
        order_item = self.get_object()
        return order_item.order and order_item.order.status == 'Pending' and self.request.user.role =="manager"
    def handle_no_permission(self):
        message.warning(self.request,"you can not update approved order")
        return redirect("orders:order_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "Update Item"
        context["btn_name"] = "Update"
        return context
    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.object.order.id})


class OrderApproveView(LoginRequiredMixin,UpdateView):
    model = Order
    fields = []
    template_name = 'orders/order_detail.html'
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if request.user.role == "manager" and order.status == 'Pending':
            order.status='Approved'
            order.approved_by=request.user
            order.save()
            for order_item in order.order_items.all(): 
                    product = order_item.product
                    product.quantity -= order_item.quantity 
                    product.save()
            message.success(request, "Order approved successfully, and product quantities updated.")
        else:
            message.error(request,"you can not approve this ")
        return redirect('orders:order_list')

