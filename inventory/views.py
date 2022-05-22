from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from .models import Inventory
from .forms import  ItemForm, DeleteForm
import requests as req
import os

# Create your views here.
def get_item(inventory_id):
    return Inventory.objects.get(inventory_id)

def inventory_list(request):
    items = Inventory.objects.all()
    for item in items:
        item.weather=_get_city_info(item.storage_location)
    data = {
        'items':items,             
    }
    return render(request, 'inventory_list.html', data)

## Typically I would protect the api key in .env file - however not working with replit so hardcoding the api key.
def _get_city_info(location):
    city_info =  req.get(f'http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid=8d168cd603dfb4f7e2e82404a4970677')
    data = city_info.json()
    latitude = data[1]['lat']
    longitude = data[1]['lon']
 
    return _get_weather(latitude, longitude)
    


def _get_weather(latitude, longitude):
    city_weather = req.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=8d168cd603dfb4f7e2e82404a4970677')
    data = city_weather.json()
    weather = data['weather'][0]['description']
    return weather
                        

def new_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)      
            item.save()
    
        return redirect('inventory_list')
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form})

def edit_item(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            item.save()

        return redirect('inventory_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form})

def temp_delete(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    if request.method == "POST":
        form = DeleteForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save()
            item.deleted=True
            item.save(update_fields=['deleted'])
        return redirect('deleted_items')
    else:
        form = DeleteForm(instance=item)
    return render(request, 'temp_delete.html', {'form': form})

def restore_deleted_item(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    if request.method == "POST":
        item.deleted=False
        item.save(update_fields=['deleted'])
        return redirect('inventory_list')
    return render(request, 'restore_item.html', {'item':item} )

def deleted_item_list(request):
    context = {'items' : Inventory.objects.all()}
    return render(request, 'deleted_items.html', context=context)



def true_delete_item(request, inventory_id):
    item = get_object_or_404(Inventory, pk=inventory_id)
    if request.method == "POST":
        item.delete()
        return HttpResponseRedirect('/')
    return render(request, 'true_delete.html')
