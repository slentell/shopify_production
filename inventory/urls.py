from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('new', views.new_item, name='new'),
    path('<int:inventory_id>/edit', views.edit_item, name='edit_item'),
    path('<int:inventory_id>/temp_delete', views.temp_delete, name='temp_delete'),
    path('<int:inventory_id>/restore', views.restore_deleted_item, name='restore_item'),
    path('<int:inventory_id>/delete', views.true_delete_item, name='true_delete_item'),
    path('deleted_items/', views.deleted_item_list, name='deleted_items')

   
    
]