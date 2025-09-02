from django.db import models
from core.models import SoftDeleteModel, TimeStampedModel

# invoicing/models.py - Invoice models (NO soft delete)
class GoldInvoice(models.Model):
    """Gold invoice model - NO soft delete"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('Cash', 'Cash'),
        ('Visa', 'Visa'),
    ]
    
    INVOICE_TYPE_CHOICES = [
        ('Sale', 'Sale'),
        ('Return Packing', 'Return Packing'),
        ('Return Unpacking', 'Return Unpacking'),
    ]
    
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='gold_invoices')
    seller = models.ForeignKey('core.Seller', on_delete=models.CASCADE, related_name='gold_invoices')
    branch = models.ForeignKey('authentication.Branch', on_delete=models.CASCADE, related_name='gold_invoices')
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, related_name='gold_invoices')
    gold_price_21 = models.DecimalField(max_digits=10, decimal_places=2)
    gold_price_24 = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES, default='Cash')
    invoice_type = models.CharField(max_length=255, choices=INVOICE_TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'gold_invoice'
    
    def __str__(self):
        return f"Gold Invoice #{self.id} - {self.customer.name}"

class GoldInvoiceItem(models.Model):
    """Gold invoice item model - NO soft delete"""
    
    invoice = models.ForeignKey(GoldInvoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_carat = models.DecimalField(max_digits=10, decimal_places=2)
    item_stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    item_quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'gold_invoice_items'
    
    def __str__(self):
        return f"{self.item_name} - Invoice #{self.invoice.id}"

class SilverInvoice(models.Model):
    """Silver invoice model - NO soft delete"""
    
    TRANSACTION_TYPE_CHOICES = [
        ('Cash', 'Cash'),
        ('Visa', 'Visa'),
    ]
    
    INVOICE_TYPE_CHOICES = [
        ('Sale', 'Sale'),
        ('Return Packing', 'Return Packing'),
        ('Return Unpacking', 'Return Unpacking'),
    ]
    
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='silver_invoices')
    seller = models.ForeignKey('core.Seller', on_delete=models.CASCADE, related_name='silver_invoices')
    branch = models.ForeignKey('authentication.Branch', on_delete=models.CASCADE, related_name='silver_invoices')
    customer = models.ForeignKey('core.Customer', on_delete=models.CASCADE, related_name='silver_invoices')
    silver_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES, default='Cash')
    invoice_type = models.CharField(max_length=255, choices=INVOICE_TYPE_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'silver_invoice'
    
    def __str__(self):
        return f"Silver Invoice #{self.id} - {self.customer.name}"

class SilverInvoiceItem(models.Model):
    """Silver invoice item model - NO soft delete"""
    
    invoice = models.ForeignKey(SilverInvoice, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    item_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_carat = models.DecimalField(max_digits=10, decimal_places=2)
    item_stamp_enduser = models.DecimalField(max_digits=10, decimal_places=2)
    item_quantity = models.BigIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'silver_invoice_items'
    
    def __str__(self):
        return f"{self.item_name} - Invoice #{self.invoice.id}"
