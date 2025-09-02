from django.db import models
from core.models import SoftDeleteModel, TimeStampedModel

# inventory/models.py - Product and stock models
class GoldProduct(SoftDeleteModel, TimeStampedModel):
    """Gold product model"""
    
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='gold_products')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    carat = models.DecimalField(max_digits=10, decimal_places=2)
    stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_unpacking = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'gold_products'
    
    def __str__(self):
        return f"{self.name} - {self.weight}g ({self.carat}K)"

class SilverProduct(SoftDeleteModel, TimeStampedModel):
    """Silver product model"""
    
    vendor = models.ForeignKey('core.Vendor', on_delete=models.CASCADE, related_name='silver_products')
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    carat = models.DecimalField(max_digits=10, decimal_places=2)
    stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=10, decimal_places=2)
    cashback_unpacking = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'silver_products'
    
    def __str__(self):
        return f"{self.name} - {self.weight}g ({self.carat}K)"

class GoldWarehouseStock(SoftDeleteModel, TimeStampedModel):
    """Gold warehouse stock model"""
    
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='gold_stocks')
    product = models.ForeignKey(GoldProduct, on_delete=models.CASCADE, related_name='warehouse_stocks')
    quantity = models.BigIntegerField()
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'gold_warehouse_stock'
        unique_together = ['warehouse', 'product']
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse.code}: {self.quantity}"

class SilverWarehouseStock(SoftDeleteModel, TimeStampedModel):
    """Silver warehouse stock model"""
    
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='silver_stocks')
    product = models.ForeignKey(SilverProduct, on_delete=models.CASCADE, related_name='warehouse_stocks')
    quantity = models.BigIntegerField()
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'silver_warehouse_stock'
        unique_together = ['warehouse', 'product']
    
    def __str__(self):
        return f"{self.product.name} - {self.warehouse.code}: {self.quantity}"
