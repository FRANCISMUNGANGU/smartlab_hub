from rest_framework.views import APIView, csrf_exempt
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .services import TransactionService
from .models import Transaction
from .serializer import TransactionSerializer
from django.conf import settings
from django.utils.decorators import method_decorator
# Create your views here.

    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'ADMIN':
                return Transaction.objects.all().order_by('-created_at')
            elif user.role == 'VENDOR':
                return Transaction.objects.filter(booking__unit__equipment__vendor=user).order_by('-created_at')
            
            return Transaction.objects.filter(booking__user=user).order_by('-created_at')
        return Transaction.objects.none()
    
