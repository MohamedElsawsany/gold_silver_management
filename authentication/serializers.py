from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer with user role and branch info"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['role'] = user.role
        token['branch_id'] = user.branch.id if user.branch else None
        token['branch_name'] = user.branch.name if user.branch else None
        token['username'] = user.username
        token['email'] = user.email
        token['is_warehouse_keeper'] = user.is_warehouse_keeper
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user info to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'is_warehouse_keeper': self.user.is_warehouse_keeper,
            'branch': {
                'id': self.user.branch.id,
                'name': self.user.branch.name
            } if self.user.branch else None
        }
        
        return data

class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Username and password are required')

class UserSerializer(serializers.ModelSerializer):
    """User serializer for read operations"""
    
    branch = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_warehouse_keeper', 'branch', 'is_active', 'created_date', 'last_login']
        read_only_fields = ['id', 'created_date', 'last_login']
    
    def get_branch(self, obj):
        if obj.branch:
            return {
                'id': obj.branch.id,
                'name': obj.branch.name
            }
        return None

class LogoutSerializer(serializers.Serializer):
    """Logout serializer"""
    
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception as e:
            raise serializers.ValidationError('Invalid token')