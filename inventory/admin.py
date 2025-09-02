from django.contrib import admin
from django.utils.html import format_html
from .models import GoldProduct, SilverProduct, GoldWarehouseStock, SilverWarehouseStock

@admin.register(GoldProduct)
class GoldProductAdmin(admin.ModelAdmin):
    """Gold product admin"""
    
    list_display = ['name', 'vendor', 'weight', 'carat', 'stamp_enduser', 'status', 'created_date']
    list_filter = ['vendor', 'carat', 'deleted_at', 'created_date']
    search_fields = ['name', 'vendor__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return GoldProduct.all_objects.get_queryset()

@admin.register(SilverProduct)
class SilverProductAdmin(admin.ModelAdmin):
    """Silver product admin"""
    
    list_display = ['name', 'vendor', 'weight', 'carat', 'stamp_enduser', 'status', 'created_date']
    list_filter = ['vendor', 'carat', 'deleted_at', 'created_date']
    search_fields = ['name', 'vendor__name']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return SilverProduct.all_objects.get_queryset()

@admin.register(GoldWarehouseStock)
class GoldWarehouseStockAdmin(admin.ModelAdmin):
    """Gold warehouse stock admin"""
    
    list_display = ['product', 'warehouse', 'quantity', 'created_by', 'status', 'updated_date']
    list_filter = ['warehouse', 'product__vendor', 'deleted_at', 'created_date']
    search_fields = ['product__name', 'warehouse__code']
    ordering = ['-updated_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return GoldWarehouseStock.all_objects.get_queryset()

@admin.register(SilverWarehouseStock)
class SilverWarehouseStockAdmin(admin.ModelAdmin):
    """Silver warehouse stock admin"""
    
    list_display = ['product', 'warehouse', 'quantity', 'created_by', 'status', 'updated_date']
    list_filter = ['warehouse', 'product__vendor', 'deleted_at', 'created_date']
    search_fields = ['product__name', 'warehouse__code']
    ordering = ['-updated_date']
    readonly_fields = ['created_date', 'updated_date']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        else:
            return format_html('<span style="color: green;">Active</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        return SilverWarehouseStock.all_objects.get_queryset()