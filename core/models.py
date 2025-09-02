from django.db import models
from .managers import SoftDeleteModel, TimeStampedModel

class Vendor(SoftDeleteModel, TimeStampedModel):
    """Vendor model"""
    
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'vendors'
    
    def __str__(self):
        return self.name

class Warehouse(SoftDeleteModel, TimeStampedModel):
    """Warehouse model"""
    
    code = models.CharField(max_length=255)
    branch = models.ForeignKey('authentication.Branch', on_delete=models.CASCADE, related_name='warehouses')
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'warehouse'
    
    def __str__(self):
        return f"{self.code} - {self.branch.name}"

class Customer(SoftDeleteModel, TimeStampedModel):
    """Customer model"""
    
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.name} - {self.phone}"

class Seller(SoftDeleteModel, TimeStampedModel):
    """Seller model"""
    
    name = models.CharField(max_length=255)
    branch = models.ForeignKey('authentication.Branch', on_delete=models.CASCADE, related_name='sellers')
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'sellers'
    
    def __str__(self):
        return f"{self.name} - {self.branch.name}"