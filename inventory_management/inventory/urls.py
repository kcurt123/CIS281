from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, check_item_by_barcode, checkout_item, items_out_list
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>/', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>/', DeleteItem.as_view(), name='delete-item'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('inventory/<int:item_id>/checkout/', checkout_item, name='checkout_item'),
    path('items-out/', items_out_list, name='items_out_list'),
    path('api/inventory/', views.update_inventory, name='update_inventory'),
    path('check-item-by-barcode/', check_item_by_barcode, name='check_item_by_barcode'),
]

