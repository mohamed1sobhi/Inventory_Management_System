from django.shortcuts import get_object_or_404, render
from .models import Shipment, ShipmentItem
from .forms import ShipmentForm,ShipmentItemFormSet
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def list_shipment(request):
    shipments = Shipment.objects.all()
    return render(request, 'shipment/list_of_shipment.html', {
        'shipments': shipments
    })

@login_required
def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    shipment_items = ShipmentItem.objects.filter(shipment=shipment)
    return render(request, 'shipment/shipment_detail.html', {
        'shipment': shipment,
        'shipment_items': shipment_items
    })

@login_required
def create_shipment(request):
    if request.method == 'POST':
        shipment_form = ShipmentForm(request.POST)
        formset = ShipmentItemFormSet(request.POST)
        if shipment_form.is_valid() and formset.is_valid():
            shipment = shipment_form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()
            shipment_items = formset.save(commit=False)
            for item in shipment_items:
                item.shipment = shipment
                item.save()
            return redirect('shipment:shipment_list')
    else:
        shipment_form = ShipmentForm()
        formset = ShipmentItemFormSet()
    return render(request, 'shipment/create_shipment.html', {
        'shipment_form': shipment_form,
        'formset': formset
    })


@login_required
def update_shipment(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if request.method == 'POST':
        shipment_form = ShipmentForm(request.POST, instance=shipment)
        formset = ShipmentItemFormSet(request.POST, instance=shipment)
        if shipment_form.is_valid() and formset.is_valid():
            shipment = shipment_form.save(commit=False)
            shipment.created_by = request.user
            shipment.save()
            shipment_items = formset.save(commit=False)
            for item in shipment_items:
                item.shipment = shipment
                item.save()
            return redirect('shipment:shipment_list')
    else:
        shipment_form = ShipmentForm(instance=shipment)
        formset = ShipmentItemFormSet(instance=shipment)
    return render(request, 'shipment/update_shipment.html', {
        'shipment_form': shipment_form,
        'formset': formset
    })
