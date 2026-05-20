from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Booking
from .serializers import BookingSerializer
from payment.services import PaymentService
from transactions.services import TransactionService
from rest_framework.response import Response
from .services import BookingService

# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            booking = BookingService.create_lab_booking(
                user=request.user,
                equipment=serializer.validated_data['unit'],
                start_date=serializer.validated_data['start_date'],
                end_date=serializer.validated_data['end_date'],
                booking_type=serializer.validated_data['booking_type'],
                pick_up_location=serializer.validated_data.get('pick_up_location'),
                drop_off_location=serializer.validated_data.get('drop_off_location'),
            )

            output_serializer = self.get_serializer(booking)
            transaction = booking.transaction
            paystack_data = PaymentService.initialize_payment(transaction)

            if paystack_data['status']:
                # 3. Send the student to Paystack
                return Response({
                    "checkout_url": paystack_data['data']['authorization_url'],
                    "reference": transaction.transaction_reference,
                    "booking data": output_serializer.data
                }, status=201)
            
            return Response({"error": "Payment initialization failed"}, status=400)
            
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'VENDOR':
                return Booking.objects.filter(unit__equipment__vendor=user)
            return Booking.objects.filter(user=user)
        return Booking.objects.none()
    
