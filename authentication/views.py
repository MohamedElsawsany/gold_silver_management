from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .serializers import LoginSerializer, LogoutSerializer, CustomTokenObtainPairSerializer
from .models import User
from django.utils import timezone

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint"""
    
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Add custom claims
        refresh['role'] = user.role
        refresh['branch_id'] = user.branch.id
        refresh['branch_name'] = user.branch.name
        refresh['username'] = user.username
        refresh['email'] = user.email
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'branch': {
                    'id': user.branch.id,
                    'name': user.branch.name
                }
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout endpoint"""
    
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'branch': {
            'id': user.branch.id,
            'name': user.branch.name
        },
        'last_login': user.last_login
    }, status=status.HTTP_200_OK)