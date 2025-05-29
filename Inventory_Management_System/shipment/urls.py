from .views import *
from django.urls import path


app_name = 'shipments'

urlpatterns = [
    path('shipment/', ShipmentListView.as_view(), name='shipment_list'),
    path('shipment/<int:pk>/', ShipmentDetailView.as_view(), name='shipment_detail'),
    path('shipment/create/', ShipmentCreateView.as_view(), name='create_shipment'),
    path('shipment/update/<int:pk>/', ShipmentUpdateView.as_view(), name='update_shipment'),
    path('shipment/delete/<int:pk>/', ShipmentDeleteView.as_view(), name='delete_shipment'),
    path('shipment/approve/<int:pk>/', ShipmentApproveView.as_view(), name='approve_shipment'),
    path('shipment/deliver/<int:pk>/', ShipmentDeliverView.as_view(), name='deliver_shipment'),
    path("add-item/<int:shipment_id>/", ShipmentItemCreateView.as_view(), name="add_shipment_item"),
]