from django.contrib import admin
from .models import GoldInvoice, GoldInvoiceItem, SilverInvoice, SilverInvoiceItem

class GoldInvoiceItemInline(admin.TabularInline):
    """Inline for gold invoice items"""
    model = GoldInvoiceItem
    extra = 0
    readonly_fields = ['item_total_price']

@admin.register(GoldInvoice)
class GoldInvoiceAdmin(admin.ModelAdmin):
    """Gold invoice admin"""
    
    list_display = ['id', 'customer', 'seller', 'branch', 'total_price', 'transaction_type', 'invoice_type', 'created_date']
    list_filter = ['transaction_type', 'invoice_type', 'branch', 'created_date']
    search_fields = ['customer__name', 'seller__name', 'id']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'total_price']
    inlines = [GoldInvoiceItemInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ['customer', 'seller', 'branch']
        return self.readonly_fields

@admin.register(GoldInvoiceItem)
class GoldInvoiceItemAdmin(admin.ModelAdmin):
    """Gold invoice item admin"""
    
    list_display = ['invoice', 'item_name', 'vendor_name', 'item_quantity', 'item_weight', 'item_total_price']
    list_filter = ['vendor_name', 'item_carat']
    search_fields = ['item_name', 'vendor_name', 'invoice__customer__name']
    ordering = ['-invoice__created_date']

class SilverInvoiceItemInline(admin.TabularInline):
    """Inline for silver invoice items"""
    model = SilverInvoiceItem
    extra = 0
    readonly_fields = ['item_total_price']

@admin.register(SilverInvoice)
class SilverInvoiceAdmin(admin.ModelAdmin):
    """Silver invoice admin"""
    
    list_display = ['id', 'customer', 'seller', 'branch', 'total_price', 'transaction_type', 'invoice_type', 'created_date']
    list_filter = ['transaction_type', 'invoice_type', 'branch', 'created_date']
    search_fields = ['customer__name', 'seller__name', 'id']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'total_price']
    inlines = [SilverInvoiceItemInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing object
            return self.readonly_fields + ['customer', 'seller', 'branch']
        return self.readonly_fields

@admin.register(SilverInvoiceItem)
class SilverInvoiceItemAdmin(admin.ModelAdmin):
    """Silver invoice item admin"""
    
    list_display = ['invoice', 'item_name', 'vendor_name', 'item_quantity', 'item_weight', 'item_total_price']
    list_filter = ['vendor_name', 'item_carat']
    search_fields = ['item_name', 'vendor_name', 'invoice__customer__name']
    ordering = ['-invoice__created_date']