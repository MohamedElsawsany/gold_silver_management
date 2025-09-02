from django.contrib import admin
from django.utils.html import format_html
from .models import Vendor, Warehouse, Customer, Seller

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Vendor admin"""
    
    list_display = ['name', 'created_by', 'status', 'created_date', 'updated_date']
    list_filter = ['deleted_at', 'created_date']
    search_fields = ['name', 'created_by__username']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return Vendor.all_objects.get_queryset()

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Warehouse admin"""
    
    list_display = ['code', 'branch', 'cash', 'created_by', 'status', 'created_date']
    list_filter = ['branch', 'deleted_at', 'created_date']
    search_fields = ['code', 'branch__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return Warehouse.all_objects.get_queryset()

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer admin"""
    
    list_display = ['name', 'phone', 'created_by', 'status', 'created_date']
    list_filter = ['deleted_at', 'created_date']
    search_fields = ['name', 'phone']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return Customer.all_objects.get_queryset()

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    """Seller admin"""
    
    list_display = ['name', 'branch', 'created_by', 'status', 'created_date']
    list_filter = ['branch', 'deleted_at', 'created_date']
    search_fields = ['name', 'branch__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return Seller.all_objects.get_queryset()