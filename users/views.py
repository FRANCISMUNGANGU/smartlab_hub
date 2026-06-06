from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from transactions import serializer
from .serializers import UserSerializer
from .models import User
from .services import UserService
from alerts.models import NotificationLog
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser


User = get_user_model()


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()  # Placeholder to avoid errors in the service layer
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to register
    http_method_names = ['post']  


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # CALL THE SERVICE
        user = UserService.register_user(serializer.validated_data)
        if not user:
            return Response({"error": "User registration failed"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "User registered successfully",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admins can see the user list    


class VendorApprovalView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            # Find the pending vendor
            vendor = User.objects.get(id=user_id, role='VENDOR')
            
            # Flip the switch
            vendor.is_active = True
            vendor.save()
            
            # Notify the vendor they are live
            NotificationLog.objects.create(
                user=vendor,
                notification_type="INFO",
                message="Your Vendor account has been verified. You can now list equipment."
            )
            
            return Response({"status": f"Vendor {vendor.username} approved."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Vendor not found."}, status=404)