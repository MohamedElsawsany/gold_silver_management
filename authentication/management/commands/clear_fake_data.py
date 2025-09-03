from django.core.management.base import BaseCommand
from django.db import transaction

from authentication.models import User, Branch
from core.models import Vendor, Warehouse, Customer, Seller
from inventory.models import GoldProduct, SilverProduct, GoldWarehouseStock, SilverWarehouseStock
from invoicing.models import GoldInvoice, GoldInvoiceItem, SilverInvoice, SilverInvoiceItem
from transactions.models import WarehouseTransaction

class Command(BaseCommand):
    help = 'Clear all fake data from database (keeps admin user)'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Clearing fake data...')
            
            # Clear in reverse dependency order
            WarehouseTransaction.objects.all().delete()
            GoldInvoiceItem.objects.all().delete()
            SilverInvoiceItem.objects.all().delete()
            GoldInvoice.objects.all().delete()
            SilverInvoice.objects.all().delete()
            GoldWarehouseStock.objects.all().delete()
            SilverWarehouseStock.objects.all().delete()
            GoldProduct.objects.all().delete()
            SilverProduct.objects.all().delete()
            Seller.objects.all().delete()
            Customer.objects.all().delete()
            Warehouse.objects.all().delete()
            Vendor.objects.all().delete()
            User.objects.exclude(username='admin').delete()
            Branch.objects.all().delete()
            
            self.stdout.write(
                self.style.SUCCESS('Successfully cleared all fake data')
            )