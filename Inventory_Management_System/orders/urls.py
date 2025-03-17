from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("create/", views.createOrder, name="create_order"),
    path("<int:order_id>/add-item/", views.add_order_item, name="add_order_item"),
    path("<int:order_id>/approve/", views.approve_order, name="approve_order"),
]