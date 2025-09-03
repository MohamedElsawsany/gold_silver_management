from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random
from decimal import Decimal
from django.utils import timezone
from datetime import timezone as dt_timezone

from authentication.models import User, Branch
from core.models import Vendor, Warehouse, Customer, Seller
from inventory.models import GoldProduct, SilverProduct, GoldWarehouseStock, SilverWarehouseStock
from invoicing.models import GoldInvoice, GoldInvoiceItem, SilverInvoice, SilverInvoiceItem
from transactions.models import WarehouseTransaction

fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with fake data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--branches',
            type=int,
            default=3,
            help='Number of branches to create'
        )
        parser.add_argument(
            '--users-per-branch',
            type=int,
            default=5,
            help='Number of users per branch'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=20,
            help='Number of products to create (gold and silver combined)'
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Creating fake data...')
            
            # Create admin user first
            admin_user = self.create_admin_user()
            
            # Create branches
            branches = self.create_branches(options['branches'], admin_user)
            
            # Create users for each branch
            users = self.create_users(branches, options['users_per_branch'])
            
            # Create vendors
            vendors = self.create_vendors(users)
            
            # Create warehouses
            warehouses = self.create_warehouses(branches, users)
            
            # Create customers
            customers = self.create_customers(users)
            
            # Create sellers
            sellers = self.create_sellers(branches, users)
            
            # Create products
            gold_products, silver_products = self.create_products(vendors, users, options['products'])
            
            # Create warehouse stocks
            self.create_warehouse_stocks(warehouses, gold_products, silver_products, users)
            
            # Create invoices
            self.create_invoices(warehouses, sellers, customers, gold_products, silver_products, users)
            
            # Create warehouse transactions
            self.create_warehouse_transactions(warehouses, users)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created:\n'
                    f'- {len(branches)} branches\n'
                    f'- {len(users)} users\n'
                    f'- {len(vendors)} vendors\n'
                    f'- {len(warehouses)} warehouses\n'
                    f'- {len(customers)} customers\n'
                    f'- {len(sellers)} sellers\n'
                    f'- {len(gold_products)} gold products\n'
                    f'- {len(silver_products)} silver products'
                )
            )

    def create_admin_user(self):
        """Create admin user if doesn't exist"""
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'Admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Created admin user (username: admin, password: admin123)')
        return admin_user

    def create_branches(self, count, admin_user):
        """Create fake branches"""
        branches = []
        branch_names = [
            'Downtown Branch', 'North Branch', 'South Branch', 'East Branch', 
            'West Branch', 'Central Branch', 'Mall Branch', 'Airport Branch'
        ]
        
        for i in range(count):
            branch = Branch.objects.create(
                name=branch_names[i] if i < len(branch_names) else f'Branch {i+1}',
                created_by=admin_user
            )
            branches.append(branch)
        
        return branches

    def create_users(self, branches, users_per_branch):
        """Create fake users"""
        users = []
        roles = ['Manager', 'Employee']
        
        for branch in branches:
            for i in range(users_per_branch):
                username = fake.user_name() + str(random.randint(100, 999))
                email = fake.email()
                role = random.choice(roles)
                
                # Ensure unique username and email
                while User.objects.filter(username=username).exists():
                    username = fake.user_name() + str(random.randint(100, 999))
                while User.objects.filter(email=email).exists():
                    email = fake.email()
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    role=role,
                    branch=branch,
                    is_active=random.choice([True, True, True, False]),  # 75% active
                    last_login=timezone.make_aware(
                        fake.date_time_between(start_date='-30d', end_date='now'),
                        timezone=dt_timezone.utc
                    )
                )
                users.append(user)
        
        return users

    def create_vendors(self, users):
        """Create fake vendors"""
        vendors = []
        vendor_names = [
            'Gold Masters Inc', 'Silver Craft Co', 'Precious Metals Ltd', 
            'Royal Jewelry Supply', 'Elite Gold Trading', 'Silver Star Corp',
            'Golden Eagle Suppliers', 'Premier Metals Group'
        ]
        
        for name in vendor_names:
            vendor = Vendor.objects.create(
                name=name,
                created_by=random.choice(users)
            )
            vendors.append(vendor)
        
        return vendors

    def create_warehouses(self, branches, users):
        """Create fake warehouses"""
        warehouses = []
        
        for branch in branches:
            # Create 1-3 warehouses per branch
            for i in range(random.randint(1, 3)):
                warehouse = Warehouse.objects.create(
                    code=f'{branch.name[:3].upper()}-WH-{i+1:02d}',
                    branch=branch,
                    cash=Decimal(str(random.uniform(10000, 100000))),
                    created_by=random.choice([u for u in users if u.branch == branch])
                )
                warehouses.append(warehouse)
        
        return warehouses

    def create_customers(self, users):
        """Create fake customers"""
        customers = []
        
        for _ in range(50):  # Create 50 customers
            customer = Customer.objects.create(
                name=fake.name(),
                phone=fake.phone_number()[:15],  # Limit to 15 chars
                created_by=random.choice(users)
            )
            customers.append(customer)
        
        return customers

    def create_sellers(self, branches, users):
        """Create fake sellers"""
        sellers = []
        
        for branch in branches:
            # Create 2-4 sellers per branch
            for _ in range(random.randint(2, 4)):
                seller = Seller.objects.create(
                    name=fake.name(),
                    branch=branch,
                    created_by=random.choice([u for u in users if u.branch == branch])
                )
                sellers.append(seller)
        
        return sellers

    def create_products(self, vendors, users, total_products):
        """Create fake gold and silver products"""
        gold_products = []
        silver_products = []
        
        # Gold product names
        gold_names = [
            'Gold Ring', 'Gold Necklace', 'Gold Bracelet', 'Gold Earrings',
            'Gold Chain', 'Gold Pendant', 'Gold Bangle', 'Gold Anklet'
        ]
        
        # Silver product names
        silver_names = [
            'Silver Ring', 'Silver Necklace', 'Silver Bracelet', 'Silver Earrings',
            'Silver Chain', 'Silver Pendant', 'Silver Bangle', 'Silver Anklet'
        ]
        
        # Create gold products (60% of total)
        gold_count = int(total_products * 0.6)
        for _ in range(gold_count):
            product = GoldProduct.objects.create(
                vendor=random.choice(vendors),
                name=random.choice(gold_names) + f' {fake.word().title()}',
                weight=Decimal(str(random.uniform(1.0, 50.0))),
                carat=Decimal(str(random.choice([14, 18, 21, 22, 24]))),
                stamp_enduser=Decimal(str(random.uniform(50, 200))),
                cashback=Decimal(str(random.uniform(10, 50))),
                cashback_unpacking=Decimal(str(random.uniform(5, 25))),
                created_by=random.choice(users)
            )
            gold_products.append(product)
        
        # Create silver products (40% of total)
        silver_count = total_products - gold_count
        for _ in range(silver_count):
            product = SilverProduct.objects.create(
                vendor=random.choice(vendors),
                name=random.choice(silver_names) + f' {fake.word().title()}',
                weight=Decimal(str(random.uniform(1.0, 100.0))),
                carat=Decimal(str(random.choice([800, 850, 900, 925, 950, 999]))),
                stamp_enduser=Decimal(str(random.uniform(20, 100))),
                cashback=Decimal(str(random.uniform(5, 25))),
                cashback_unpacking=Decimal(str(random.uniform(2, 15))),
                created_by=random.choice(users)
            )
            silver_products.append(product)
        
        return gold_products, silver_products

    def create_warehouse_stocks(self, warehouses, gold_products, silver_products, users):
        """Create fake warehouse stocks"""
        
        # Create gold stocks
        for warehouse in warehouses:
            # Stock 60-80% of gold products in each warehouse
            products_to_stock = random.sample(
                gold_products, 
                k=random.randint(int(len(gold_products) * 0.6), int(len(gold_products) * 0.8))
            )
            
            for product in products_to_stock:
                GoldWarehouseStock.objects.create(
                    warehouse=warehouse,
                    product=product,
                    quantity=random.randint(1, 100),
                    created_by=random.choice([u for u in users if u.branch == warehouse.branch])
                )
        
        # Create silver stocks
        for warehouse in warehouses:
            # Stock 60-80% of silver products in each warehouse
            products_to_stock = random.sample(
                silver_products, 
                k=random.randint(int(len(silver_products) * 0.6), int(len(silver_products) * 0.8))
            )
            
            for product in products_to_stock:
                SilverWarehouseStock.objects.create(
                    warehouse=warehouse,
                    product=product,
                    quantity=random.randint(1, 200),
                    created_by=random.choice([u for u in users if u.branch == warehouse.branch])
                )

    def create_invoices(self, warehouses, sellers, customers, gold_products, silver_products, users):
        """Create fake invoices"""
        
        # Create gold invoices
        for _ in range(30):  # Create 30 gold invoices
            warehouse = random.choice(warehouses)
            seller = random.choice([s for s in sellers if s.branch == warehouse.branch])
            
            # Get available gold products for this warehouse
            available_stocks = GoldWarehouseStock.objects.filter(
                warehouse=warehouse,
                quantity__gt=0
            )
            
            if available_stocks.exists():
                invoice = GoldInvoice.objects.create(
                    warehouse=warehouse,
                    seller=seller,
                    branch=warehouse.branch,
                    customer=random.choice(customers),
                    gold_price_21=Decimal(str(random.uniform(60, 80))),
                    gold_price_24=Decimal(str(random.uniform(70, 90))),
                    total_price=Decimal('0'),  # Will be calculated
                    transaction_type=random.choice(['Cash', 'Visa']),
                    invoice_type=random.choice(['Sale', 'Return Packing', 'Return Unpacking']),
                    created_by=random.choice([u for u in users if u.branch == warehouse.branch])
                )
                
                # Create invoice items
                total = Decimal('0')
                num_items = random.randint(1, 5)
                selected_stocks = random.sample(list(available_stocks), 
                                              min(num_items, len(available_stocks)))
                
                for stock in selected_stocks:
                    quantity = random.randint(1, min(stock.quantity, 10))
                    item_price = Decimal(str(random.uniform(100, 1000)))
                    item_total = item_price * quantity
                    
                    GoldInvoiceItem.objects.create(
                        invoice=invoice,
                        item_name=stock.product.name,
                        item_weight=stock.product.weight,
                        item_carat=stock.product.carat,
                        item_stamp_enduser=stock.product.stamp_enduser,
                        item_quantity=quantity,
                        item_price=item_price,
                        item_total_price=item_total,
                        vendor_name=stock.product.vendor.name
                    )
                    total += item_total
                
                invoice.total_price = total
                invoice.save()

        # Create silver invoices
        for _ in range(20):  # Create 20 silver invoices
            warehouse = random.choice(warehouses)
            seller = random.choice([s for s in sellers if s.branch == warehouse.branch])
            
            # Get available silver products for this warehouse
            available_stocks = SilverWarehouseStock.objects.filter(
                warehouse=warehouse,
                quantity__gt=0
            )
            
            if available_stocks.exists():
                invoice = SilverInvoice.objects.create(
                    warehouse=warehouse,
                    seller=seller,
                    branch=warehouse.branch,
                    customer=random.choice(customers),
                    silver_price=Decimal(str(random.uniform(0.5, 2.0))),
                    total_price=Decimal('0'),  # Will be calculated
                    transaction_type=random.choice(['Cash', 'Visa']),
                    invoice_type=random.choice(['Sale', 'Return Packing', 'Return Unpacking']),
                    created_by=random.choice([u for u in users if u.branch == warehouse.branch])
                )
                
                # Create invoice items
                total = Decimal('0')
                num_items = random.randint(1, 5)
                selected_stocks = random.sample(list(available_stocks), 
                                              min(num_items, len(available_stocks)))
                
                for stock in selected_stocks:
                    quantity = random.randint(1, min(stock.quantity, 20))
                    item_price = Decimal(str(random.uniform(20, 200)))
                    item_total = item_price * quantity
                    
                    SilverInvoiceItem.objects.create(
                        invoice=invoice,
                        item_name=stock.product.name,
                        item_weight=stock.product.weight,
                        item_carat=stock.product.carat,
                        item_stamp_enduser=stock.product.stamp_enduser,
                        item_quantity=quantity,
                        item_price=item_price,
                        item_total_price=item_total,
                        vendor_name=stock.product.vendor.name
                    )
                    total += item_total
                
                invoice.total_price = total
                invoice.save()

    def create_warehouse_transactions(self, warehouses, users):
        """Create fake warehouse transactions"""
        for _ in range(15):  # Create 15 transactions
            from_warehouse = random.choice(warehouses)
            to_warehouse = random.choice([w for w in warehouses if w != from_warehouse])
            
            WarehouseTransaction.objects.create(
                item_name=random.choice([
                    'Gold Ring Set', 'Silver Necklace Collection', 
                    'Gold Bracelet Batch', 'Silver Earrings Set'
                ]),
                from_warehouse=from_warehouse,
                to_warehouse=to_warehouse,
                quantity=random.randint(1, 50),
                status=random.choice(['Pending', 'Approved', 'Rejected']),
                created_by=random.choice([u for u in users if u.branch == from_warehouse.branch]),
                action_by=random.choice([u for u in users if u.role in ['Admin', 'Manager']])
            )