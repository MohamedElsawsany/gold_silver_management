from rest_framework import serializers
from .models import Vendor, Warehouse, Customer, Seller
from authentication.models import Branch, User


class VendorSerializer(serializers.ModelSerializer):
    """Vendor serializer"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

class BranchSerializer(serializers.ModelSerializer):
    """Branch serializer"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'name', 'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

class WarehouseSerializer(serializers.ModelSerializer):
    """Warehouse serializer"""
    
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Warehouse
        fields = ['id', 'code', 'branch', 'branch_name', 'cash', 'created_by', 
                 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_branch(self, value):
        """Validate branch access for non-admin users"""
        request = self.context.get('request')
        if request and request.user.role != 'Admin':
            if request.user.branch != value:
                raise serializers.ValidationError("You can only create warehouses in your own branch.")
        return value

class CustomerSerializer(serializers.ModelSerializer):
    """Customer serializer"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'created_by', 'created_by_username', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

class SellerSerializer(serializers.ModelSerializer):
    """Seller serializer"""
    
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Seller
        fields = ['id', 'name', 'branch', 'branch_name', 'created_by', 
                 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_branch(self, value):
        """Validate branch access for non-admin users"""
        request = self.context.get('request')
        if request and request.user.role != 'Admin':
            if request.user.branch != value:
                raise serializers.ValidationError("You can only create sellers in your own branch.")
        return value