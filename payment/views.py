from rest_framework.views import APIView, csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.utils.decorators import method_decorator
from .services import PaymentService
from .signals import payment_confirmed
from transactions.models import Transaction
import logging
from django.shortcuts import redirect
from django.contrib import messages

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        signature = request.headers.get('x-paystack-signature')
        payload = request.body

        # 🔐 Step 1: Verify signature
        if not PaymentService.verify_webhook(payload, signature):
            logger.warning("Invalid Paystack signature")
            return Response({"error": "Invalid signature"}, status=401)

        data = request.data

        # 🔎 Step 2: Only care about success events
        if data.get('event') != 'charge.success':
            return Response({"status": "ignored"}, status=200)

        reference = data['data']['reference']

        try:
            # 🔎 Step 3: Find transaction
            txn = Transaction.objects.get(transaction_reference=reference)

            # 💾 Step 4: Save payment (idempotent)
            PaymentService.create_payment(txn, data)

            # ⚙️ Step 5: Process success (idempotent)
            PaymentService.process_successful_payment(txn.id)
            # payment_confirmed.send(sender=self.__class__, transaction=txn.id)

            return Response({"status": "success"}, status=200)

        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {reference}")
            return Response({"error": "Transaction not found"}, status=404)

        except Exception as e:
            logger.error(f"Webhook failure: {str(e)}")
            return Response({"error": "Server error"}, status=500)

class PaystackCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        reference = request.query_params.get('reference')
        frontend_url = f"http://localhost/bookings?status=success&reference={reference}"
    
        return redirect(frontend_url)
       