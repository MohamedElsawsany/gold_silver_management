from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Branch

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    
    list_display = ['username', 'email', 'role', 'branch', 'is_active', 'status', 'last_login']
    list_filter = ['role', 'branch', 'is_active', 'deleted_at', 'created_at']
    search_fields = ['username', 'email', 'branch__name']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'role', 'branch')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'branch', 'is_active'),
        }),
    )
    
    readonly_fields = ['created_at', 'last_login']
    
    def status(self, obj):
        if obj.deleted_at:
            return format_html('<span style="color: red;">Deleted</span>')
        elif obj.is_active:
            return format_html('<span style="color: green;">Active</span>')
        else:
            return format_html('<span style="color: orange;">Inactive</span>')
    status.short_description = 'Status'
    
    def get_queryset(self, request):
        # Show all users including soft-deleted ones in admin
        return User.all_objects.get_queryset()

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Branch admin"""
    
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
        return Branch.all_objects.get_queryset()