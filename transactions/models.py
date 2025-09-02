from django.db import models
from core.models import SoftDeleteModel, TimeStampedModel

# transactions/models.py - Warehouse transaction model
class WarehouseTransaction(models.Model):
    """Warehouse transaction model - NO soft delete"""
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    item_name = models.CharField(max_length=255)
    from_warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='incoming_transactions')
    quantity = models.BigIntegerField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='created_transactions')
    action_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='actioned_transactions')
    action_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'warehouse_transactions'
    
    def __str__(self):
        return f"{self.item_name}: {self.from_warehouse.code} → {self.to_warehouse.code} ({self.status})"