from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.getSuppliersList, name='list_supplier'),
    path('create/', views.createSupplier, name='create_supplier'),
    path('edit/<int:supplier_id>',
         views.editSupplier, name='edit_supplier'),
    path('delete/<int:supplier_id>', views.softDeleteSupplier, name='delete_supplier'),
]
