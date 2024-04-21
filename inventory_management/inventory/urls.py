from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem, check_item_by_barcode, checkout_item, checked_out_items, return_item
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', Index.as_view(), name='index'),  # Home page, typically a landing page
    path('dashboard/', Dashboard.as_view(), name='dashboard'),  # Main dashboard view
    path('add-item/', AddItem.as_view(), name='add-item'),  # Add a new item
    path('edit-item/<int:pk>/', EditItem.as_view(), name='edit-item'),  # Edit an existing item
    path('delete-item/<int:pk>/', DeleteItem.as_view(), name='delete-item'),  # Delete an item
    path('signup/', SignUpView.as_view(), name='signup'),  # Signup page for new users
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),  # Login page
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Logout process
    path('inventory/<int:item_id>/checkout/', checkout_item, name='checkout_item'),  # Checkout an inventory item
    path('checked-out/', checked_out_items, name='checked-out-items'),
    path('api/inventory/', views.update_inventory, name='update_inventory'),  # API endpoint for inventory updates
    path('check-item-by-barcode/', check_item_by_barcode, name='check_item_by_barcode'),  # API for checking item by barcode
    path('return-item/<int:item_id>/', return_item, name='return_item'),
]