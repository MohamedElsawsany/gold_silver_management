from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from core.models import SoftDeleteModel, TimeStampedModel


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')
        extra_fields.setdefault('is_warehouse_keeper', False)  # Default to False for superuser
        
        return self.create_user(username, email, password, **extra_fields)

class Branch(SoftDeleteModel, TimeStampedModel):
    """Branch model"""
    
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_branches')
    
    class Meta:
        db_table = 'branches'
        verbose_name_plural = 'Branches'
    
    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin, SoftDeleteModel):
    """Custom User model"""
    
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    ]
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_warehouse_keeper = models.BooleanField(default=False)  # New field
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        keeper_suffix = " (Warehouse Keeper)" if self.is_warehouse_keeper else ""
        return f"{self.username} ({self.role}){keeper_suffix}"