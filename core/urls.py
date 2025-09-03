from django.urls import path
from . import views

urlpatterns = [
    # Vendor endpoints
    path('vendors/', views.vendor_list_create, name='vendor_list_create'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    
    # Branch endpoints
    path('branches/', views.branch_list_create, name='branch_list_create'),
    path('branches/<int:pk>/', views.branch_detail, name='branch_detail'),
    
    # Warehouse endpoints
    path('warehouses/', views.warehouse_list_create, name='warehouse_list_create'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    
    # Customer endpoints
    path('customers/', views.customer_list_create, name='customer_list_create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    
    # Seller endpoints
    path('sellers/', views.seller_list_create, name='seller_list_create'),
    path('sellers/<int:pk>/', views.seller_detail, name='seller_detail'),
]