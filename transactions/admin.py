from django.contrib import admin
from django.utils.html import format_html
from .models import WarehouseTransaction

@admin.register(WarehouseTransaction)
class WarehouseTransactionAdmin(admin.ModelAdmin):
    """Warehouse transaction admin"""
    
    list_display = ['item_name', 'from_warehouse', 'to_warehouse', 'quantity', 'status_display', 'created_by', 'action_by', 'created_date']
    list_filter = ['status', 'from_warehouse__branch', 'to_warehouse__branch', 'created_date']
    search_fields = ['item_name', 'from_warehouse__code', 'to_warehouse__code']
    ordering = ['-created_date']
    readonly_fields = ['created_date', 'action_date']
    
    def status_display(self, obj):
        color_map = {
            'Pending': 'orange',
            'Approved': 'green',
            'Rejected': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            color_map.get(obj.status, 'black'),
            obj.status
        )
    status_display.short_description = 'Status'
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status != 'Pending':
            return self.readonly_fields + ['from_warehouse', 'to_warehouse', 'quantity', 'item_name']
        return self.readonly_fields