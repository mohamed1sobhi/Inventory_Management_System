from django.urls import path
from .views import *

app_name = "orders"

urlpatterns = [
    path("all_orders/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("create/", OrderCreateView.as_view(), name="create_order"),
    path("add-item/<int:order_id>/", OrderItemCreateView.as_view(), name="add_order_item"),
    path("approve/<int:pk>/", OrderApproveView.as_view(), name="approve_order"),
    path("update-item/<int:pk>/", OrderUpdateView.as_view(), name="update_order_item"), 
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="delete_order"),
]