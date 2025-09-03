from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Vendor, Warehouse, Customer, Seller
from authentication.models import Branch
from authentication.permissions import (
    IsAdminUser, IsManagerOrAdmin, IsSameBranchOrAdmin,
    IsManagerWarehouseKeeperOrAdmin
)
from .serializers import (
    VendorSerializer, WarehouseSerializer, CustomerSerializer, 
    SellerSerializer, BranchSerializer
)


# ============= VENDOR ENDPOINTS =============

@api_view(['GET', 'POST'])
@permission_classes([IsManagerOrAdmin])
def vendor_list_create(request):
    """List all vendors or create new vendor"""
    
    if request.method == 'GET':
        # Filter vendors for non-admin users
        if request.user.role == 'Admin':
            vendors = Vendor.objects.all()
        else:
            vendors = Vendor.objects.filter(created_by__branch=request.user.branch)
        
        # Search functionality
        search = request.GET.get('search', '')
        if search:
            vendors = vendors.filter(
                Q(name__icontains=search)
            )
        
        # Pagination
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(vendors, page_size)
        vendors_page = paginator.get_page(page)
        
        serializer = VendorSerializer(vendors_page, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'page': int(page),
            'page_size': int(page_size),
            'total_pages': paginator.num_pages
        })
    
    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsSameBranchOrAdmin])
def vendor_detail(request, pk):
    """Retrieve, update or delete vendor"""
    
    vendor = get_object_or_404(Vendor, pk=pk)
    
    # Check permissions
    if request.user.role != 'Admin' and vendor.created_by.branch != request.user.branch:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        vendor.delete()
        return Response({'message': 'Vendor deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


# ============= BRANCH ENDPOINTS =============

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def branch_list_create(request):
    """List all branches or create new branch - Admin only"""
    
    if request.method == 'GET':
        branches = Branch.objects.all()
        
        # Search functionality
        search = request.GET.get('search', '')
        if search:
            branches = branches.filter(Q(name__icontains=search))
        
        # Pagination
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(branches, page_size)
        branches_page = paginator.get_page(page)
        
        serializer = BranchSerializer(branches_page, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'page': int(page),
            'page_size': int(page_size),
            'total_pages': paginator.num_pages
        })
    
    elif request.method == 'POST':
        serializer = BranchSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def branch_detail(request, pk):
    """Retrieve, update or delete branch - Admin only"""
    
    branch = get_object_or_404(Branch, pk=pk)
    
    if request.method == 'GET':
        serializer = BranchSerializer(branch)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BranchSerializer(branch, data=request.data, partial=True, 
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        branch.delete()
        return Response({'message': 'Branch deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


# ============= WAREHOUSE ENDPOINTS =============

@api_view(['GET', 'POST'])
@permission_classes([IsManagerOrAdmin])
def warehouse_list_create(request):
    """List all warehouses or create new warehouse"""
    
    if request.method == 'GET':
        # Filter warehouses for non-admin users
        if request.user.role == 'Admin':
            warehouses = Warehouse.objects.all()
        else:
            warehouses = Warehouse.objects.filter(branch=request.user.branch)
        
        # Search functionality
        search = request.GET.get('search', '')
        if search:
            warehouses = warehouses.filter(
                Q(code__icontains=search) | Q(branch__name__icontains=search)
            )
        
        # Pagination
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(warehouses, page_size)
        warehouses_page = paginator.get_page(page)
        
        serializer = WarehouseSerializer(warehouses_page, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'page': int(page),
            'page_size': int(page_size),
            'total_pages': paginator.num_pages
        })
    
    elif request.method == 'POST':
        serializer = WarehouseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsSameBranchOrAdmin])
def warehouse_detail(request, pk):
    """Retrieve, update or delete warehouse"""
    
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    # Check permissions
    if request.user.role != 'Admin' and warehouse.branch != request.user.branch:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = WarehouseSerializer(warehouse)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = WarehouseSerializer(warehouse, data=request.data, partial=True,
                                       context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        warehouse.delete()
        return Response({'message': 'Warehouse deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


# ============= CUSTOMER ENDPOINTS =============

@api_view(['GET', 'POST'])
@permission_classes([IsManagerWarehouseKeeperOrAdmin])
def customer_list_create(request):
    """List all customers or create new customer"""
    
    if request.method == 'GET':
        # Filter customers for non-admin users
        if request.user.role == 'Admin':
            customers = Customer.objects.all()
        else:
            customers = Customer.objects.filter(created_by__branch=request.user.branch)
        
        # Search functionality
        search = request.GET.get('search', '')
        if search:
            customers = customers.filter(
                Q(name__icontains=search) | Q(phone__icontains=search)
            )
        
        # Pagination
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(customers, page_size)
        customers_page = paginator.get_page(page)
        
        serializer = CustomerSerializer(customers_page, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'page': int(page),
            'page_size': int(page_size),
            'total_pages': paginator.num_pages
        })
    
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsSameBranchOrAdmin])
def customer_detail(request, pk):
    """Retrieve, update or delete customer"""
    
    customer = get_object_or_404(Customer, pk=pk)
    
    # Check permissions
    if request.user.role != 'Admin' and customer.created_by.branch != request.user.branch:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        customer.delete()
        return Response({'message': 'Customer deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)


# ============= SELLER ENDPOINTS =============

@api_view(['GET', 'POST'])
@permission_classes([IsManagerOrAdmin])
def seller_list_create(request):
    """List all sellers or create new seller"""
    
    if request.method == 'GET':
        # Filter sellers for non-admin users
        if request.user.role == 'Admin':
            sellers = Seller.objects.all()
        else:
            sellers = Seller.objects.filter(branch=request.user.branch)
        
        # Search functionality
        search = request.GET.get('search', '')
        if search:
            sellers = sellers.filter(
                Q(name__icontains=search) | Q(branch__name__icontains=search)
            )
        
        # Pagination
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(sellers, page_size)
        sellers_page = paginator.get_page(page)
        
        serializer = SellerSerializer(sellers_page, many=True)
        
        return Response({
            'results': serializer.data,
            'count': paginator.count,
            'page': int(page),
            'page_size': int(page_size),
            'total_pages': paginator.num_pages
        })
    
    elif request.method == 'POST':
        serializer = SellerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsSameBranchOrAdmin])
def seller_detail(request, pk):
    """Retrieve, update or delete seller"""
    
    seller = get_object_or_404(Seller, pk=pk)
    
    # Check permissions
    if request.user.role != 'Admin' and seller.branch != request.user.branch:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = SellerSerializer(seller)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = SellerSerializer(seller, data=request.data, partial=True,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        seller.delete()
        return Response({'message': 'Seller deleted successfully'}, 
                       status=status.HTTP_204_NO_CONTENT)