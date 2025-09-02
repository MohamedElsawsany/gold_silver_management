from django.db import models
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted objects by default"""
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class AllObjectsManager(models.Manager):
    """Manager that includes all objects, even soft-deleted ones"""
    
    def get_queryset(self):
        return super().get_queryset()

class SoftDeleteModel(models.Model):
    """Abstract base model with soft delete functionality"""
    
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()
    
    class Meta:
        abstract = True
    
    def delete(self, using=None, keep_parents=False):
        """Soft delete by setting deleted_at timestamp"""
        self.deleted_at = timezone.now()
        self.save(using=using)
    
    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete the object"""
        super().delete(using=using, keep_parents=keep_parents)
    
    def restore(self):
        """Restore a soft-deleted object"""
        self.deleted_at = None
        self.save()

class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps"""
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True